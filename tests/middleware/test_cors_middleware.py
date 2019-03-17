import os

from masonite.middleware import CorsMiddleware
from masonite.app import App
from masonite.request import Request
from masonite.testsuite import generate_wsgi, TestSuite

from config import middleware


class TestCorsMiddleware:

    def setup_method(self):
        self.request = Request(generate_wsgi())
        self.middleware = CorsMiddleware(self.request)
        self.app = TestSuite().create_container().container
        self.app.bind('Request', self.request.load_app(self.app))
        self.request = self.app.make('Request')

    def test_secure_headers_middleware(self):
        self.middleware.CORS = {"Access-Control-Allow-Origin": "*"}
        self.middleware.after()
        assert self.request.header('Access-Control-Allow-Origin') == '*'
