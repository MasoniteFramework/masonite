from masonite.request import Request
from masonite.view import View
from masonite.auth.Csrf import Csrf
from masonite.app import App
from middleware.CsrfMiddleware import CsrfMiddleware
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