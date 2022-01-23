import os
from src.masonite.exceptions.exceptions import RouteNotFoundException

from tests import TestCase
from src.masonite.routes import Route


class TestHttpRequests(TestCase):
    
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test-with-input", "WelcomeController@form_with_input"),
        )
        
    def test_csrf_request(self):
        self.withoutCsrf()
        return self.post("/").assertContains("Welcome")

    def test_route_not_found_throw_exception_in_dev_mode(self):
        os.environ["APP_ENV"] = "development"

        with self.assertRaises(RouteNotFoundException) as e:
            self.get("/unknown/route")

        self.assertEqual(str(e.exception), "GET /unknown/route : 404 Not Found")

    def test_route_not_found_has_404_status(self):
        self.get("/unknown/route").assertNotFound()

    def test_old_helper(self):
        self.get("/test-with-input", {"name": "Sam"})
        assert self.application.make("request").old("name") == "Sam"
        assert self.application.make("request").old("wrong-input") == ""
