from tests import TestCase
from src.masonite.routes import Route


class TestHttpRequests(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test/users/@id", "WelcomeController@show_user"),
        )

    def test_csrf_request(self):
        self.withoutCsrf()
        return self.post("/").assertContains("Welcome")

    def test_find_or_fail(self):
        self.get("/test/users/1").assertOk()
        self.get("/test/users/10").assertNotFound()
