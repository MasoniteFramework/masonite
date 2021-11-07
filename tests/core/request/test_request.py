from tests import TestCase
from src.masonite.request import Request
from src.masonite.utils.http import generate_wsgi
import os


class TestRequest(TestCase):
    def test_request_can_get_path(self):
        request = Request(generate_wsgi(path="/test"))
        self.assertEqual(request.get_path(), "/test")
        self.assertEqual(request.get_request_method(), "GET")

    def test_request_contains(self):
        request = Request(generate_wsgi(path="/test"))
        self.assertTrue(request.contains("/test"))

        request = Request(generate_wsgi(path="/test/user"))
        self.assertTrue(request.contains("/test/*"))

        request = Request(generate_wsgi(path="/test/admin/user"))
        self.assertTrue(request.contains("/test/*/user"))

        request = Request(generate_wsgi(path="/test/admin/user"))
        self.assertTrue(request.contains("*"))
