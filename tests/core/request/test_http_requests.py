import os
from src.masonite.exceptions.exceptions import RouteNotFoundException

from tests import TestCase


class TestHttpRequests(TestCase):
    def test_csrf_request(self):
        self.withoutCsrf()
        return self.post("/").assertContains("Welcome")

    def test_route_not_found_throw_exception_in_dev_mode(self):
        os.environ["APP_ENV"] = "development"
        with self.assertRaises(RouteNotFoundException) as e:
            self.get("/unknown/route")

        self.assertEqual(str(e.exception), "GET /unknown/route : 404 Not Found")
