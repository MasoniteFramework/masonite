from masonite.app import App
from masonite.middleware import CsrfMiddleware
from masonite.auth.Csrf import Csrf
from masonite.testsuite.TestSuite import TestSuite


class TestCsrf:
    def setup_method(self):
        self.app = TestSuite().create_container().container
        self.app.bind('Csrf', Csrf(self.app.make('Request')))
        self.csrf = self.app.make('Csrf')
        self.request = self.app.make('Request')
        middleware = self.app.resolve(CsrfMiddleware)

        middleware.before()

    def test_middleware_sets_csrf_cookie(self):
        assert self.request.get_cookie('csrf_token', decrypt=False)

    def test_middleware_shares_view(self):
        assert 'csrf_field' in self.app.make('ViewClass').dictionary
        assert 'input' in self.app.make('ViewClass').dictionary['csrf_field']

    def test_middleware_does_not_need_safe_filter(self):
        assert '&lt;' not in self.app.make('ViewClass').render('csrf_field').rendered_template

    def test_verify_token(self):
        token = self.request.get_cookie('csrf_token', decrypt=False)
        assert self.csrf.verify_csrf_token(token)
