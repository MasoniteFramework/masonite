""" Test Secure Headers Midddleware """
import unittest

from src.masonite.middleware import SecureHeadersMiddleware
from src.masonite.request import Request
from src.masonite.testing import TestCase, generate_wsgi


class TestSecureHeadersMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.request = Request(generate_wsgi())
        self.middleware = SecureHeadersMiddleware(self.request)
        self.container.bind('Request', self.request.load_app(self.container))
        self.request = self.container.make('Request')

    def test_secure_headers_middleware(self):
        self.middleware.after()
        self.assertEqual(self.request.header('Strict-Transport-Security'), 'max-age=63072000; includeSubdomains')
        self.assertEqual(self.request.header('X-Frame-Options'), 'SAMEORIGIN')

    def test_secure_headers_gets_middleware_from_the_config(self):
        self.request = self.container.make('Request')
        self.middleware.after()
        self.assertEqual(self.request.header('X-Content-Type-Options'), 'sniff-test')
