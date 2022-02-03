import json
import io
import os
import sys
import unittest
import pendulum
from contextlib import contextmanager

from ..routes import Route
from ..foundation.response_handler import testcase_handler
from ..utils.http import generate_wsgi
from ..request import Request
from ..response import Response
from ..environment import LoadEnvironment
from ..facades import Config
from ..providers.RouteProvider import RouteProvider
from ..exceptions import RouteNotFoundException
from .TestCommand import TestCommand


class TestCase(unittest.TestCase):
    routes_to_restore = ()

    def setUp(self):
        LoadEnvironment("testing")
        from wsgi import application

        self.application = application
        self.original_class_mocks = {}
        self._test_cookies = {}
        self._test_headers = {}
        if hasattr(self, "startTestRun"):
            self.startTestRun()
        self.withoutCsrf()
        self._exception_handling = False
        # boot providers as they won't not be loaded if the test is not doing a request
        self.application.bind("environ", generate_wsgi())
        try:
            for provider in self.application.get_providers():
                # if no request is made we don't need RouteProvider, and we can't load it anyway
                # because we don't have created a CSRF token yet
                if not isinstance(provider, RouteProvider):
                    application.resolve(provider.boot)
        except Exception as e:
            if not self._exception_handling:
                raise e
            self.application.make("exception_handler").handle(e)

        self.routes_to_restore = set(self.application.make("router").routes)

    def tearDown(self):
        # be sure to reset this between each test
        self._exception_handling = False
        # restore routes
        if self.routes_to_restore:
            self.application.make("router").routes = list(self.routes_to_restore)
        if hasattr(self, "stopTestRun"):
            self.stopTestRun()

    def withExceptionsHandling(self):
        """Enable for the duration of a test the handling of exceptions through the exception
        handler."""
        self._exception_handling = True

    def withoutExceptionsHandling(self):
        """Disable handling of exceptions."""
        self._exception_handling = False

    def setRoutes(self, *routes):
        """Set all routes of router during lifetime of a test."""
        self.application.make("router").set(Route.group(*routes, middleware=["web"]))
        return self

    def addRoutes(self, *routes):
        """Add routes to router during lifetime of a test."""
        self.application.make("router").add(Route.group(*routes, middleware=["web"]))
        return self

    def withCsrf(self):
        self._csrf = True
        return self

    def withoutCsrf(self):
        self._csrf = False
        return self

    def get(self, route, data=None):
        return self.fetch(route, data, method="GET")

    def post(self, route, data=None):
        return self.fetch(route, data, method="POST")

    def put(self, route, data=None):
        return self.fetch(route, data, method="PUT")

    def patch(self, route, data=None):
        return self.fetch(route, data, method="PATCH")

    def make_request(
        self, data={}, path="/", query_string="application=Masonite", method="GET"
    ):
        request = Request(generate_wsgi(data, path, query_string, method))
        request.app = self.application

        self.application.bind("request", request)
        return request

    def make_response(self, data={}):
        request = Response(generate_wsgi(data))
        request.app = self.application

        self.application.bind("response", request)
        return request

    def fetch(self, path, data=None, method=None):
        if data is None:
            data = {}
        if not self._csrf:
            token = self.application.make("sign").sign("cookie")
            data.update({"__token": "cookie"})
            wsgi_request = generate_wsgi(
                {
                    "HTTP_COOKIE": f"SESSID={token}; csrf_token={token}",
                    "CONTENT_LENGTH": len(str(json.dumps(data))),
                    "REQUEST_METHOD": method,
                    "PATH_INFO": path,
                    "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
                }
            )
        else:
            wsgi_request = generate_wsgi(
                {
                    "CONTENT_LENGTH": len(str(json.dumps(data))),
                    "REQUEST_METHOD": method,
                    "PATH_INFO": path,
                    "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
                }
            )

        request, response = testcase_handler(
            self.application,
            wsgi_request,
            self.mock_start_response,
            exception_handling=self._exception_handling,
        )
        # add eventual cookies added inside the test (not encrypted to be able to assert value ?)
        for name, value in self._test_cookies.items():
            request.cookie(name, value)
        # add eventual headers added inside the test
        for name, value in self._test_headers.items():
            request.header(name, value)

        route = self.application.make("router").find(path, method)
        if route:
            return self.application.make("tests.response").build(
                self.application, request, response, route
            )

        exception = RouteNotFoundException(f"No route found for url {path}")
        if self._exception_handling:
            response = self.application.make("exception_handler").handle(exception)
            return self.application.make("tests.response").build(
                self.application, request, response, route
            )
        else:
            raise exception

    def mock_start_response(self, *args, **kwargs):
        pass

    @contextmanager
    def captureOutput(self):
        new_out, new_err = io.StringIO(), io.StringIO()
        # save normal system output
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout
        finally:
            # restore system output
            sys.stdout, sys.stderr = old_out, old_err

    @contextmanager
    def debugMode(self, enabled=True):
        old_debug_mode = Config.get("application.debug")
        Config.set("application.debug", enabled)
        yield
        Config.set("application.debug", old_debug_mode)

    @contextmanager
    def env(self, environment):
        old_env = os.getenv("APP_ENV", "")
        os.environ["APP_ENV"] = environment
        yield
        os.environ["APP_ENV"] = old_env

    def craft(self, command, arguments_str=""):
        """Run a given command in tests and obtain a TestCommand instance to assert command
        outputs.
        self.craft("controller", "Welcome").assertSuccess()
        """
        return TestCommand(self.application).run(command, arguments_str)

    def fake(self, binding):
        """Mock a service with its mocked implementation or with a given custom
        one."""

        # save original first
        self.original_class_mocks.update(
            {binding: self.application.make(binding, self.application)}
        )
        # mock by overriding with mocked version
        mock = self.application.make(f"mock.{binding}", self.application)
        self.application.bind(binding, mock)
        return mock

    def withCookies(self, cookies_dict):
        self._test_cookies = cookies_dict
        return self

    def withHeaders(self, headers_dict):
        self._test_headers = headers_dict
        return self

    def actingAs(self, user):
        self.make_request()
        self.application.make("auth").guard("web").login_by_id(
            user.get_primary_key_value()
        )

    def restore(self, binding):
        """Restore the service previously mocked to the original one."""
        original = self.original_class_mocks.get(binding)
        self.application.bind(binding, original)

    def fakeTime(self, pendulum_datetime):
        """Set a given pendulum instance to be returned when a "now" (or "today", "tomorrow",
        "yesterday") instance is created. It's really useful during tests to check
        timestamps logic."""
        pendulum.set_test_now(pendulum_datetime)

    def fakeTimeTomorrow(self):
        """Set the mocked time as tomorrow."""
        self.fakeTime(pendulum.tomorrow())

    def fakeTimeYesterday(self):
        """Set the mocked time as yesterday."""
        self.fakeTime(pendulum.yesterday())

    def fakeTimeInFuture(self, offset, unit="days"):
        """Set the mocked time as an offset of days in the future. Unit can be specified
        among pendulum units: seconds, minutes, hours, days, weeks, months, years."""
        self.restoreTime()
        datetime = pendulum.now().add(**{unit: offset})
        self.fakeTime(datetime)

    def fakeTimeInPast(self, offset, unit="days"):
        """Set the mocked time as an offset of days in the past. Unit can be specified
        among pendulum units: seconds, minutes, hours, days, weeks, months, years."""
        self.restoreTime()
        datetime = pendulum.now().subtract(**{unit: offset})
        self.fakeTime(datetime)

    def restoreTime(self):
        """Restore time to correct one, so that pendulum new "now" instance are corrects.
        This method will be typically called in tearDown() method of a test class."""
        # this will clear the mock
        pendulum.set_test_now()

    def assertDatabaseCount(self, table, count):
        self.assertEqual(self.application.make("builder").table(table).count(), count)

    def assertDatabaseHas(self, table, query_dict):
        self.assertGreaterEqual(
            self.application.make("builder").table(table).where(query_dict).count(), 1
        )

    def assertDatabaseMissing(self, table, query_dict):
        self.assertEqual(
            self.application.make("builder").table(table).where(query_dict).count(), 0
        )

    def assertDeleted(self, instance):
        self.assertFalse(
            self.application.make("builder")
            .table(instance.get_table_name())
            .where(instance.get_primary_key(), instance.get_primary_key_value())
            .get()
        )

    def assertSoftDeleted(self, instance):
        deleted_at_column = instance.get_deleted_at_column()
        self.assertTrue(
            self.application.make("builder")
            .table(instance.get_table_name())
            .where(instance.get_primary_key(), instance.get_primary_key_value())
            .where_not_null(deleted_at_column)
            .get()
        )
