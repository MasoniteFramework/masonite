from src.masonite.middleware import CorsMiddleware
from src.masonite.request import Request
from src.masonite.testsuite import generate_wsgi, TestSuite

import unittest


class TestCorsMiddleware(unittest.TestCase):

    def setUp(self):
        self.request = Request(generate_wsgi())
        self.middleware = CorsMiddleware(self.request)
        self.app = TestSuite().create_container().container
        self.app.bind('Request', self.request.load_app(self.app))
        self.request = self.app.make('Request')

    def test_secure_headers_middleware(self):
        self.middleware.CORS = {"Access-Control-Allow-Origin": "*"}
        self.middleware.before()
        self.assertEqual(self.request.header('Access-Control-Allow-Origin'), '*')
