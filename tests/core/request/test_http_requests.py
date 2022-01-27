from tests import TestCase
from src.masonite.routes import Route, HTTPRoute


class TestHttpRequests(TestCase):
    def test_csrf_request(self):
        self.withoutCsrf()
        return self.post("/").assertContains("Welcome")

    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test-with-input", "WelcomeController@form_with_input"),
        )

    def test_old_helper(self):
        self.get("/test-with-input", {"name": "Sam"})
        assert self.application.make("request").old("name") == "Sam"
        assert self.application.make("request").old("wrong-input") == ""

    def test_get_route(self):
        self.get("/")
        route = self.application.make("request").get_route()
        assert isinstance(route, HTTPRoute)
