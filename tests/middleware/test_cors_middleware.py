from src.masonite.middleware import CorsMiddleware
from src.masonite.request import Request
from src.masonite.testing import generate_wsgi, TestCase

import unittest


class TestCorsMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.container.bind('Request', Request(generate_wsgi()).load_app(self.container))
        self.request = self.container.make('Request')
        self.middleware = self.container.resolve(CorsMiddleware)

    def test_secure_headers_middleware(self):
        self.middleware.CORS = {"Access-Control-Allow-Origin": "*"}
        self.middleware.before()
        self.assertEqual(self.request.header('Access-Control-Allow-Origin'), '*')
