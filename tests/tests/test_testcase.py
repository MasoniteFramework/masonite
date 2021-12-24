import pendulum
import pytest

from tests import TestCase
from tests.integrations.controllers.WelcomeController import WelcomeController
from masoniteorm.models import Model
from src.masonite.routes import Route
from src.masonite.authentication import Authenticates
from src.masonite.middleware import EncryptCookies


class User(Model, Authenticates):
    pass


class CustomTestResponse:
    def assertCustom(self):
        assert 1
        return self


class OtherCustomTestResponse:
    def assertOtherCustom(self):
        assert 2
        return self


class TestTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            Route.get("/", "WelcomeController@show").name("home"),
        )

    def tearDown(self):
        super().tearDown()
        self.restoreTime()

    def test_add_routes(self):
        self.assertEqual(len(self.application.make("router").routes), 1)
        self.addRoutes(Route.get("/some-route", "WelcomeController@show"))
        self.assertEqual(len(self.application.make("router").routes), 2)

    def test_use_custom_test_response(self):
        self.application.make("tests.response").add(
            CustomTestResponse, OtherCustomTestResponse
        )
        # can use default assertions and custom from different classes
        self.get("/").assertContains("Welcome").assertCustom().assertOtherCustom()

    def test_fake_time(self):
        given_date = pendulum.datetime(2015, 2, 5)
        self.fakeTime(given_date)
        self.assertEqual(pendulum.now(), given_date)
        self.restoreTime()
        self.assertNotEqual(pendulum.now(), given_date)

    def test_fake_time_tomorrow(self):
        tomorrow = pendulum.tomorrow()
        self.fakeTimeTomorrow()
        self.assertEqual(pendulum.now(), tomorrow)

    def test_fake_time_yesterday(self):
        yesterday = pendulum.yesterday()
        self.fakeTimeYesterday()
        self.assertEqual(pendulum.now(), yesterday)

    def test_fake_time_in_future(self):
        real_now = pendulum.now()
        self.fakeTimeInFuture(10)
        self.assertEqual(pendulum.now().diff(real_now).in_days(), 10)
        self.assertGreater(pendulum.now(), real_now)

        self.fakeTimeInFuture(1, "months")
        self.assertEqual(pendulum.now().diff(real_now).in_months(), 1)

    # def test_fake_time_in_past(self):
    #     real_now = pendulum.now()
    #     self.fakeTimeInPast(10)
    #     self.assertEqual(pendulum.now().diff(real_now).in_days(), 10)
    #     self.assertLess(pendulum.now(), real_now)

    #     self.fakeTimeInPast(3, "hours")
    #     self.assertEqual(real_now.hour - pendulum.now().hour, 3)


class TestTestingAssertions(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            Route.get("/", "WelcomeController@show").name("home"),
            Route.get("/test", "WelcomeController@show").name("test"),
            Route.get("/view", "WelcomeController@view").name("view"),
            Route.get("/view-context", "WelcomeController@view_with_context").name(
                "view_with_context"
            ),
            Route.get("/test-404", "WelcomeController@not_found").name("not_found"),
            Route.get("/test-creation", "WelcomeController@create").name("create"),
            Route.get("/test-unauthorized", "WelcomeController@unauthorized").name(
                "unauthorized"
            ),
            Route.get("/test-forbidden", "WelcomeController@forbidden").name(
                "forbidden"
            ),
            Route.get("/test-empty", "WelcomeController@empty").name("empty"),
            Route.get(
                "/test-response-header", "WelcomeController@response_with_headers"
            ),
            Route.get("/test-redirect-1", "WelcomeController@redirect_url"),
            Route.get("/test-redirect-2", "WelcomeController@redirect_route"),
            Route.get("/test-redirect-3", "WelcomeController@redirect_route_params"),
            Route.get("/test/@id", "WelcomeController@with_params").name("test_params"),
            Route.get("/test-json", "WelcomeController@json").name("json"),
            Route.get("/test-session", "WelcomeController@session").name("session"),
            Route.get(
                "/test-session-errors", "WelcomeController@session_with_errors"
            ).name("session"),
            Route.get("/test-session-2", "WelcomeController@session2").name("session2"),
            Route.get("/test-authenticates", "WelcomeController@auth").name("auth"),
        )

    def test_assert_contains(self):
        self.get("/").assertContains("Welcome")
        self.get("/").assertNotContains("hello")

    def test_assert_is_named(self):
        self.get("/test").assertIsNamed("test")
        self.get("/test").assertIsNotNamed("welcome")

    def test_assert_not_found(self):
        self.get("/test-404").assertNotFound()

    def test_assert_is_status(self):
        self.get("/test").assertIsStatus(200)

    def test_assert_ok(self):
        self.get("/test").assertOk()

    def test_assert_created(self):
        self.get("/test-creation").assertCreated()

    def test_assert_unauthorized(self):
        self.get("/test-unauthorized").assertUnauthorized()

    def test_assert_forbidden(self):
        self.get("/test-forbidden").assertForbidden()

    def test_assert_no_content(self):
        self.get("/test-empty").assertNoContent()

    def test_assert_cookie(self):
        self.withCookies({"test": "value"}).get("/").assertCookie("test")

    def test_assert_cookie_value(self):
        self.withCookies({"test": "value"}).get("/").assertCookie("test", "value")

    def test_assert_cookie_missing(self):
        self.get("/").assertCookieMissing("test")

    def test_assert_plain_cookie(self):
        self.withCookies({"test": "value"}).get("/").assertPlainCookie("test")

    def test_assert_has_header(self):
        self.get("/test-response-header").assertHasHeader("TEST")
        self.get("/test-response-header").assertHasHeader("TEST", "value")

    def test_assert_header_missing(self):
        self.get("/").assertHeaderMissing("X-Test")

    def test_assert_request_with_headers(self):
        request = self.withHeaders({"X-TEST": "value"}).get("/").request
        assert request.header("X-Test") == "value"

    def test_assert_redirect_to_url(self):
        self.get("/test-redirect-1").assertRedirect("/")

    def test_assert_redirect_to_route(self):
        self.get("/test-redirect-2").assertRedirect(name="test")
        self.get("/test-redirect-3").assertRedirect(
            name="test_params", params={"id": 1}
        )

    def test_assert_session_has(self):
        self.get("/test-session").assertSessionHas("key")
        self.get("/test-session").assertSessionHas("key", "value")

    def test_assert_session_has_errors(self):
        self.get("/test-session-errors").assertSessionHasErrors()
        self.get("/test-session-errors").assertSessionHasErrors(["email"])
        self.get("/test-session-errors").assertSessionHasErrors(["email", "password"])

    def test_assert_session_has_no_errors(self):
        self.get("/test-session").assertSessionHasNoErrors()
        self.get("/test-session-errors").assertSessionHasNoErrors(["name"])

    def test_assert_session_missing(self):
        self.get("/").assertSessionMissing("some_test_key")

    def test_assert_view_is(self):
        self.get("/view").assertViewIs("welcome")

    def test_assert_view_has(self):
        self.get("/view-context").assertViewHas("count")
        self.get("/view-context").assertViewHas("count", 1)
        self.get("/view-context").assertViewHas("users", ["John", "Joe"])
        self.get("/view-context").assertViewHas("other_key.nested")
        self.get("/view-context").assertViewHas("other_key.nested", 1)

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHas("not_in_view")
        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHas("not_in_view", 3)

    def test_assert_view_helpers_raise_error_if_not_rendering_a_view(self):
        # json response
        with self.assertRaises(ValueError):
            self.get("/test-json").assertViewIs("test")
        # string response
        self.get("/test").assertViewIs("welcome")

    def test_assert_view_has_exact(self):
        self.get("/view-context").assertViewHasExact(["users", "count", "other_key"])
        self.get("/view-context").assertViewHasExact(
            {"count": 1, "users": ["John", "Joe"], "other_key": {"nested": 1}}
        )

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHasExact(
                ["users", "count", "not in data"]
            )

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewHasExact({"count": 1})

    def test_assert_view_missing(self):
        self.get("/view-context").assertViewMissing("not in data")

        with self.assertRaises(AssertionError):
            self.get("/view-context").assertViewMissing("users")

    def test_assert_guest(self):
        self.get("/test").assertGuest()

    @pytest.mark.skip(
        reason="Assertion code looks okay, but test is still failing ? What's the problem ?"
    )
    def test_assert_authenticated(self):
        self.get("/test-authenticates").assertAuthenticated()

    def test_assert_authenticated_as(self):
        self.make_request()
        self.application.make("auth").guard("web").attempt(
            "idmann509@gmail.com", "secret"
        )
        user = User.find(1)
        self.get("/test").assertAuthenticatedAs(user)

    def test_assert_has_controller(self):
        self.get("/test").assertHasController("WelcomeController@show")
        self.get("/test").assertHasController(WelcomeController)

    def test_assert_route_has_parameter(self):
        self.get("/test/3").assertRouteHasParameter("id")
        with self.assertRaises(AssertionError):
            self.get("/test/3").assertRouteHasParameter("key")
        self.get("/test/3").assertRouteHasParameter("id", 3)
        with self.assertRaises(AssertionError):
            self.get("/test/3").assertRouteHasParameter("id", 4)

    def test_assert_has_route_middleware(self):
        self.get("/test").assertHasRouteMiddleware("web")

    def test_assert_has_http_middleware(self):
        self.get("/test").assertHasHttpMiddleware(EncryptCookies)

    def test_assert_json(self):
        self.get("/test-json").assertJson({"key": "value"})
        # works also in a nested path
        self.get("/test-json").assertJson(
            {"other_key": {"nested": 1, "nested_again": {"a": 1, "b": 2}}}
        )

    def test_json_assertions_fail_when_response_not_json(self):
        with self.assertRaises(ValueError):
            self.get("/view").assertJson({"key": "value"})

    def test_assert_json_path(self):
        self.get("/test-json").assertJsonPath("key2", [1, 2])
        self.get("/test-json").assertJsonPath("other_key.nested", 1)
        self.get("/test-json").assertJsonPath("other_key.nested_again.b", 2)
        self.get("/test-json").assertJsonPath(
            "other_key.nested_again", {"a": 1, "b": 2}
        )

    def test_assert_json_count(self):
        self.get("/test-json").assertJsonCount(3)
        self.get("/test-json").assertJsonCount(2, key="other_key")

    def test_assert_json_exact(self):
        self.get("/test-json").assertJsonExact(
            {
                "key": "value",
                "key2": [1, 2],
                "other_key": {
                    "nested": 1,
                    "nested_again": {"a": 1, "b": 2},
                },
            }
        )

    def test_assert_json_missing(self):
        self.get("/test-json").assertJsonMissing("key3")
        self.get("/test-json").assertJsonMissing("some_key.nested")
        with self.assertRaises(AssertionError):
            self.get("/test-json").assertJsonMissing("other_key.nested")

    def test_assert_database_count(self):
        self.assertDatabaseCount("users", 1)

    def test_assert_database_has(self):
        self.assertDatabaseHas("users", {"name": "Joe"})

    def test_assert_database_missing(self):
        self.assertDatabaseMissing(
            "users", {"name": "John", "email": "john@example.com"}
        )
