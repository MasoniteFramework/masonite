import unittest

from masonite.auth.Csrf import Csrf
from masonite.middleware import CsrfMiddleware
from masonite.testsuite.TestSuite import TestSuite


class TestCsrf(unittest.TestCase):
    
    def setUp(self):
        self.app = TestSuite().create_container().container
        self.app.bind('Csrf', Csrf(self.app.make('Request')))
        self.csrf = self.app.make('Csrf')
        self.request = self.app.make('Request')
        middleware = self.app.resolve(CsrfMiddleware)

        middleware.before()

    def test_middleware_sets_csrf_cookie(self):
        self.assertTrue(self.request.get_cookie('csrf_token', decrypt=False))

    def test_middleware_shares_view(self):
        self.assertIn('csrf_field', self.app.make('ViewClass')._shared)
        self.assertIn('input', self.app.make('ViewClass')._shared['csrf_field'])

    def test_middleware_does_not_need_safe_filter(self):
        self.assertNotIn('&lt;', self.app.make('ViewClass').render('csrf_field').rendered_template)

    def test_verify_token(self):
        token = self.request.get_cookie('csrf_token', decrypt=False)
        self.assertTrue(self.csrf.verify_csrf_token(token))
