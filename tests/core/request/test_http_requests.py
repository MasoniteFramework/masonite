from tests import TestCase
from src.masonite.routes import Route, HTTPRoute
from src.masonite.exceptions.exceptions import RouteNotFoundException


class TestHttpRequests(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test-with-input", "WelcomeController@form_with_input"),
            Route.get("/server-error", "WelcomeController@server_error"),
        )

    def test_csrf_request(self):
        self.withoutCsrf()
        return self.post("/").assertContains("Welcome")

    def test_route_not_found_throw_exception_in_debug_mode(self):
        with self.debugMode():
            with self.assertRaises(RouteNotFoundException) as e:
                self.get("/unknown/route")

            self.assertEqual(str(e.exception), "GET /unknown/route : 404 Not Found")

    def test_route_not_found_with_debug_off(self):
        self.withExceptionsHandling()  # enable exception handler
        with self.debugMode(False):
            self.get("/unknown/route").assertNotFound().assertViewIs("errors/404")

    def test_server_error_with_debug_off(self):
        self.withExceptionsHandling()  # enable exception handler
        with self.debugMode(False):
            self.get("/server-error").assertError().assertViewIs("errors/500")

    def test_server_error_with_debug_on(self):
        with self.debugMode():
            with self.assertRaises(Exception):
                self.get("/server-error")

    def test_old_helper(self):
        self.get("/test-with-input", {"name": "Sam"})
        assert self.application.make("request").old("name") == "Sam"
        assert self.application.make("request").old("wrong-input") == ""

    def test_get_route(self):
        self.get("/")
        route = self.application.make("request").get_route()
        assert isinstance(route, HTTPRoute)
