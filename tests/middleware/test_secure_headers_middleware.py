""" Test Maintenance Mode Midddleware """
import os

from masonite.app import App
from masonite.request import Request
from masonite.middleware import SecureHeadersMiddleware
from masonite.testsuite import generate_wsgi

from config import middleware


class TestSecureHeadersMiddleware:

    def setup_method(self):
        self.request = Request(generate_wsgi())
        self.middleware = SecureHeadersMiddleware(self.request)

    def test_secure_headers_middleware(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('StatusCode', '200 OK')
        request = app.make('Request').load_app(app)
        self.middleware.after()
        assert request.header('Strict-Transport-Security') == 'max-age=63072000; includeSubdomains'
        assert request.header('X-Frame-Options') == 'SAMEORIGIN'