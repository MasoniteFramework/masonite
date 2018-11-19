from masonite.request import Request
from masonite.view import View
from masonite.auth.Csrf import Csrf
from masonite.app import App
from masonite.middleware import CsrfMiddleware
from masonite.testsuite.TestSuite import generate_wsgi
import pytest
from masonite.exceptions import InvalidCSRFToken


class TestCSRFMiddleware:

    def setup_method(self):
        self.app = App()
        self.request = Request(generate_wsgi())
        self.view = View(self.app)
        self.app.bind('Request', self.request)

        self.request = self.app.make('Request')

        self.middleware = CsrfMiddleware(self.request, Csrf(self.request), self.view)

    def test_middleware_shares_correct_input(self):
        self.middleware.before()
        assert 'csrf_field' in self.view.dictionary
        assert self.view.dictionary['csrf_field'].startswith("<input type='hidden' name='__token' value='")

    def test_middleware_throws_exception_on_post(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.middleware.exempt = []
        with pytest.raises(InvalidCSRFToken):
            self.middleware.before()

    def test_incoming_token_does_not_throw_exception_with_token(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.request_variables.update({'__token': self.request.get_cookie('csrf_token')})
        self.middleware.exempt = []
        self.middleware.before()

    def test_generates_csrf_token(self):
        assert len(self.middleware.generate_token()) == 30

    def test_generates_token_every_request(self):
        token1 = self.middleware.verify_token()
        token2 = self.middleware.verify_token()

        assert len(token1) == 30
        assert len(token2) == 30
        assert token1 != token2

    def test_does_not_generate_token_every_request(self):
        self.middleware.every_request = False
        token1 = self.middleware.verify_token()
        token2 = self.middleware.verify_token()

        assert len(token1) == 30
        assert len(token2) == 30
        assert token1 == token2
