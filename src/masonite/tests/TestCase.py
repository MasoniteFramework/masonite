import json
import io
import os
from pprint import pprint
import sys
import pytest
import unittest
import pendulum
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any
from pprint import pprint


if TYPE_CHECKING:
    from ..foundation import Application
    from ..routes import HTTPRoute
    from .HttpTestResponse import HttpTestResponse
    from pendulum import DateTime
    from masoniteorm.models import Model

from ..cookies import CookieJar
from ..routes import Route
from ..utils.http import generate_wsgi
from ..request import Request
from ..headers import HeaderBag, Header
from ..response import Response
from ..environment import LoadEnvironment
from ..facades import Config, Session
from ..providers.RouteProvider import RouteProvider
from ..providers.FrameworkProvider import FrameworkProvider
from ..exceptions import RouteNotFoundException
from .TestCommand import TestCommand


class TestCase(unittest.TestCase):
    routes_to_restore = ()

    def setUp(self):
        """Define code that should be run before each unit tests."""
        LoadEnvironment("testing")
        from wsgi import application

        self.application: "Application" = application
        self.original_class_mocks = {}

        self._acting_as = {}
        self._test_cookies = {}
        self._test_headers = {}
        self._test_session = {}
        self._console_out = None
        self._console_err = None

        if hasattr(self, "startTestRun"):
            self.startTestRun()

        if hasattr(self, "connection") and self.connection:
            self.application.make("resolver")._connection_details["default"] = self.connection

        self.withoutCsrf()

        self.withoutExceptionsHandling()
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
        """Define code that should be run after each unit tests."""
        self.withoutCsrf()
        self.withoutExceptionsHandling()
        self._acting_as = {}
        self._test_cookies = {}
        self._test_session = {}
        self._test_headers = {}

        # restore routes
        if self.routes_to_restore:
            self.application.make("router").routes = list(self.routes_to_restore)
        if hasattr(self, "stopTestRun"):
            self.stopTestRun()

        # restore console output
        self._console_out = None
        self._console_err = None

        # logout users
        self.application.make("auth").logout()

    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        """Add all useful pytest fixtures to unittest.
        In the future, when needed more pytest fixtures could be integrated to Masonite TestCase.
        """
        # 'capsys' fixture allow to read output/error from stdout/stderr
        self.capsys = capsys

    def _readConsoleOutput(self):
        """Read console output if it has not been read yet."""
        if self._console_out is None and self._console_err is None:
            output = self.capsys.readouterr()
            self._console_out = output.out
            self._console_err = output.err

    def assertConsoleEmpty(self) -> "TestCase":
        """Assert that nothing (output or error) has been printed to the console."""
        self._readConsoleOutput()
        self.assertEqual("", self._console_out)
        self.assertEqual("", self._console_err)
        return self

    def assertConsoleNotEmpty(self) -> "TestCase":
        """Assert that something (output or error) has been printed to the console."""
        self._readConsoleOutput()
        assert self._console_out != "" or self._console_err != ""
        return self

    def assertConsoleExactOutput(self, output: str) -> "TestCase":
        """Assert that console standard output is equal to given output."""
        self._readConsoleOutput()
        self.assertEqual(output, self._console_out)
        return self

    def assertConsoleOutputContains(self, output: str) -> "TestCase":
        """Assert that console standard output contains given output."""
        self._readConsoleOutput()
        self.assertIn(output, self._console_out)
        return self

    def assertConsoleOutputMissing(self, output: str) -> "TestCase":
        """Assert that console standard output does not contain the given output."""
        self._readConsoleOutput()
        self.assertNotIn(output, self._console_out)
        return self

    def assertConsoleHasErrors(self) -> "TestCase":
        """Assert that something has been output to console standard error."""
        self._readConsoleOutput()
        self.assertNotEqual(self._console_err, "")
        return self

    def assertConsoleExactError(self, error: str) -> "TestCase":
        """Assert that console standard error is equal to given error."""
        self._readConsoleOutput()
        self.assertEqual(error, self._console_err)
        return self

    def assertConsoleErrorContains(self, error: str) -> "TestCase":
        """Assert that console standard error contains given error."""
        self._readConsoleOutput()
        self.assertIn(error, self._console_err)
        return self

    def withExceptionsHandling(self) -> None:
        """Enable for the duration of a test the handling of exceptions through Masonite exception
        handler."""
        self._exception_handling = True

    def withoutExceptionsHandling(self) -> None:
        """Disable handling of exceptions with Masonite exception handler. Exceptions will be
        raised directly in the tests. This is the default behaviour."""
        self._exception_handling = False

    def setRoutes(self, *routes: "HTTPRoute") -> None:
        """Set all routes of router during lifetime of a test."""
        self.application.make("router").set(Route.group(*routes, middleware=["web"]))
        return self

    def addRoutes(self, *routes: "HTTPRoute") -> None:
        """Add routes to router during lifetime of a test."""
        self.application.make("router").add(Route.group(*routes, middleware=["web"]))
        return self

    def withCsrf(self) -> None:
        """Enable CSRF verification during lifetime of a test"""
        self._csrf = True
        return self

    def withoutCsrf(self) -> None:
        """Disable CSRF verification during lifetime of a test. This is the default behaviour."""
        self._csrf = False
        return self

    def get(self, route: str, data=None):
        """Make a GET request route"""
        return self.fetch(route, data, method="GET")

    def post(self, route: str, data=None):
        return self.fetch(route, data, method="POST")

    def put(self, route: str, data=None):
        return self.fetch(route, data, method="PUT")

    def patch(self, route: str, data=None):
        return self.fetch(route, data, method="PATCH")

    def head(self, route, data=None):
        return self.fetch(route, data, method="HEAD")

    def options(self, route, data=None):
        return self.fetch(route, data, method="OPTIONS")

    def make_request(
        self,
        wsgi_data: dict = {},
        post_data: dict = {},
        path: str = "/",
        query_string: str = "application=Masonite",
        method: str = "GET",
    ) -> "Request":

        wsgi_environ = {
            **wsgi_data,
            "wsgi.input": io.BytesIO(bytes(json.dumps(post_data), "utf-8")),
            "CONTENT_LENGTH": len(str(json.dumps(post_data))),
        }
        request = Request(generate_wsgi(wsgi_environ, path, query_string, method))
        request.app = self.application

        self.application.bind("request", request)
        return request

    def make_response(self, data: dict = {}) -> "Response":
        response = Response(generate_wsgi(data))
        response.app = self.application

        self.application.bind("response", response)
        return response

    def fetch(
        self, path: str, data: dict = None, method: str = None
    ) -> "HttpTestResponse":
        """Run an HTTP request and get a test response on which assertions can be run."""
        # prepare WSGI request environment
        if data is None:
            data = {}

        if not self._csrf:
            token = self.application.make("sign").sign("cookie")
            data.update({"__token": "cookie"})
            http_cookie = f"SESSID={token}; csrf_token={token}"

        environ = generate_wsgi(
            {
                "CONTENT_LENGTH": len(str(json.dumps(data))),
                "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
                "HTTP_COOKIE": http_cookie,
            },
            path=path,
            method=method,
        )
        self.application.bind("environ", environ)

        # boot all WSGI providers
        try:
            for provider in self.application.get_providers():
                if isinstance(provider, FrameworkProvider):
                    self.application.resolve(provider.boot)
                    # now we have a request, response object
                    request = self.application.make("request")

                    # add eventual cookies added inside the test (not encrypted to be able to assert value ?)
                    for name, value in self._test_cookies.items():
                        request.cookie(name, value)

                    # add eventual headers added inside the test
                    for name, value in self._test_headers.items():
                        request.header(name, value)

                    # @dev: this is impossible for now because session is started in the session middleware only...
                    # add eventual session data added inside the test
                    # for name, value in self._test_session.items():
                    #     Session.set(name, value)

                    # log user if required
                    if self._acting_as:
                        user = self._acting_as.get("user")
                        guard = self._acting_as.get("guard")
                        self.application.make("auth").guard(guard).attempt_by_id(
                            user.get_primary_key_value()
                        )
                else:
                    self.application.resolve(provider.boot)

        except Exception as e:
            if not self._exception_handling:
                raise e
            self.application.make("exception_handler").handle(e)

        response = self.application.make("response")

        self.mock_start_response(
            response.get_status_code(),
            response.get_headers() + response.cookie_jar.render_response(),
        )

        route = self.application.make("router").find(path, method)
        if route:
            return self.application.make("tests.response").build(
                self, self.application, request, response, route
            )

        exception = RouteNotFoundException(f"No route found for url {path}")
        if self._exception_handling:
            response = self.application.make("exception_handler").handle(exception)
            return self.application.make("tests.response").build(
                self, self.application, request, response, route
            )
        else:
            raise exception

    def mock_start_response(self, *args, **kwargs):
        pass

    @contextmanager
    def captureOutput(self):
        """Capture standard output (stdout/stderr) of a Masonite command."""
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
    def debugMode(self, enabled: bool = True):
        """Set application debug mode."""
        old_debug_mode = Config.get("application.debug")
        Config.set("application.debug", enabled)
        yield
        Config.set("application.debug", old_debug_mode)

    @contextmanager
    def env(self, environment: str):
        """Set application environment."""
        old_env = os.getenv("APP_ENV", "")
        os.environ["APP_ENV"] = environment
        yield
        os.environ["APP_ENV"] = old_env

    def craft(self, command: str, arguments_str: str = "") -> "TestCommand":
        """Run a given command in tests and obtain a TestCommand instance to assert command
        outputs.
        Example:
            self.craft("controller", "Welcome").assertSuccess()
        """
        return TestCommand(self.application).run(command, arguments_str)

    def fake(self, binding: "str") -> Any:
        """Mock a service in the container with its mocked implementation or with a given custom
        one."""

        # save original first
        self.original_class_mocks.update(
            {binding: self.application.make(binding, self.application)}
        )
        # mock by overriding with mocked version
        mock = self.application.make(f"mock.{binding}", self.application)
        if hasattr(mock, "reset"):
            mock.reset()
        self.application.bind(binding, mock)
        return mock

    def withCookies(self, cookies_dict: dict) -> "TestCase":
        """Add cookies to the request during the lifetime of the test."""
        self._test_cookies = cookies_dict
        return self

    def withHeaders(self, headers_dict: dict) -> "TestCase":
        """Add headers to the request during the lifetime of the test."""
        self._test_headers = headers_dict
        return self

    # def withSession(self, session_dict: dict) -> "TestCase":
    #     """Add session data to the request during the lifetime of the test."""
    #     self._test_session = session_dict
    #     return self

    def actingAs(self, user, guard="web") -> "TestCase":
        """Connect as the given user during the lifetime of the test. You can select the auth
        guard to use to authenticate."""
        self.application.bind("test_user", user)
        self._acting_as = {"user": user, "guard": guard}
        return self

    def actingAsGuest(self) -> "TestCase":
        """Connect as an unauthenticated user during the lifetime of the test."""
        self.application.make("auth").logout()
        self._acting_as = {}
        return self

    def restore(self, binding: str) -> None:
        """Restore the service previously mocked to the original one."""
        original = self.original_class_mocks.get(binding)
        self.application.bind(binding, original)

    def fakeTime(self, pendulum_datetime: "DateTime" = None) -> "DateTime":
        """Set a given pendulum instance to be returned when a "now" (or "today", "tomorrow",
        "yesterday") instance is created. It's really useful during tests to check
        timestamps logic."""
        if pendulum_datetime is None:
            pendulum_datetime = pendulum.now()
        pendulum.set_test_now(pendulum_datetime)
        return pendulum_datetime

    def fakeTimeTomorrow(self) -> None:
        """Set the mocked time as tomorrow."""
        self.fakeTime(pendulum.tomorrow())

    def fakeTimeYesterday(self) -> None:
        """Set the mocked time as yesterday."""
        self.fakeTime(pendulum.yesterday())

    def fakeTimeInFuture(self, offset: int, unit: str = "days") -> None:
        """Set the mocked time as an offset of days in the future. Unit can be specified
        among pendulum units: seconds, minutes, hours, days, weeks, months, years."""
        self.restoreTime()
        datetime = pendulum.now().add(**{unit: offset})
        self.fakeTime(datetime)

    def fakeTimeInPast(self, offset: int, unit: str = "days") -> None:
        """Set the mocked time as an offset of days in the past. Unit can be specified
        among pendulum units: seconds, minutes, hours, days, weeks, months, years."""
        self.restoreTime()
        datetime = pendulum.now().subtract(**{unit: offset})
        self.fakeTime(datetime)

    def restoreTime(self) -> None:
        """Restore time to correct one, so that pendulum new "now" instance are corrects.
        This method will be typically called in tearDown() method of a test class."""
        # this will clear the mock
        pendulum.set_test_now()

    def assertDatabaseCount(self, table: str, count: int) -> None:
        self.assertEqual(self.application.make("builder").table(table).count(), count)

    def assertDatabaseHas(self, table: str, query_dict: dict) -> None:
        self.assertGreaterEqual(
            self.application.make("builder").table(table).where(query_dict).count(), 1
        )

    def assertDatabaseMissing(self, table: str, query_dict: dict) -> None:
        self.assertEqual(
            self.application.make("builder").table(table).where(query_dict).count(), 0
        )

    def assertDeleted(self, instance: "Model") -> None:
        self.assertFalse(
            self.application.make("builder")
            .table(instance.get_table_name())
            .where(instance.get_primary_key(), instance.get_primary_key_value())
            .get()
        )

    def assertSoftDeleted(self, instance: "Model") -> None:
        deleted_at_column = instance.get_deleted_at_column()
        self.assertTrue(
            self.application.make("builder")
            .table(instance.get_table_name())
            .where(instance.get_primary_key(), instance.get_primary_key_value())
            .where_not_null(deleted_at_column)
            .get()
        )

    def dump(self, output: str, title: str = ""):
        """Print output to console during tests. A title can be provided to be displayed at dump
        start."""
        with self.capsys.disabled():
            print("\n")
            if title:
                print(f"\033[93m> {title}:\033[0m\n")
            pprint(output, width=110)

    def stop(self, msg: str = ""):
        """Stop current test, a message can be given and will be displayed in the
        console.

        2 is the pytest exit code for user interruption.
        https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
        """
        return pytest.exit(msg, 2)
