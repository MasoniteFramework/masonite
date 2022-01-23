from tests import TestCase
from src.masonite.routes import Route


class TestHttpRequests(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test/users/@id", "WelcomeController@show_user"),
            Route.get("/test-with-input", "WelcomeController@form_with_input"),
        )

    def test_csrf_request(self):
        self.withoutCsrf()
        return self.post("/").assertContains("Welcome")

    def test_find_or_fail_during_request(self):
        self.get("/test/users/1").assertOk()
        self.get("/test/users/10").assertNotFound()

    def test_old_helper(self):
        self.get("/test-with-input", {"name": "Sam"})
        assert self.application.make("request").old("name") == "Sam"
        assert self.application.make("request").old("wrong-input") == ""
