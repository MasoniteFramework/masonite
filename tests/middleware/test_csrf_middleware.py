from src.masonite.request import Request
from src.masonite.view import View
from src.masonite.auth.Csrf import Csrf
from src.masonite.app import App
from src.masonite.middleware import CsrfMiddleware
from src.masonite.exceptions import InvalidCSRFToken
from src.masonite.routes import Get, Route, Post
import unittest
from src.masonite.testing import TestCase, generate_wsgi


class TestCSRFMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.buildOwnContainer()
        self.middleware = CsrfMiddleware
        self.withHttpMiddleware([
            self.middleware,
        ])
        self.routes(only=[
            Post('/test/@route', 'TestController@show'),
            Get('/test/10', 'TestController@show'),
            Post('/', 'TestController@show'),
        ])

        self.withCsrf()

    def test_middleware_shares_correct_input(self):
        container = self.get('/test/10').container
        self.assertIn('csrf_field', container.make('ViewClass')._shared)
        self.assertTrue(container.make('ViewClass')._shared['csrf_field'].startswith("<input type='hidden' name='__token' value='"))

    def test_middleware_throws_exception_on_post(self):
        with self.assertRaises(InvalidCSRFToken):
            self.post('/')

    def test_middleware_can_accept_param_route(self):
        self.middleware.exempt = [
            '/test/@route'
        ]

        self.post('/test/1')

    def test_middleware_can_exempt(self):
        self.middleware.exempt = [
            '/test/1'
        ]
        self.post('/test/1')

    def test_middleware_throws_exeption_on_wrong_route(self):
        self.middleware.exempt = [
            '/test/2'
        ]

        with self.assertRaises(InvalidCSRFToken):
            self.post('/test/11')

    def test_incoming_token_does_not_throw_exception_with_token(self):
        self.middleware.exempt = []
        self.withoutCsrf()
        self.post('/test/11')

    def test_generates_csrf_token(self):
        self.assertTrue(len(self.get('/test/10').request.get_cookie('csrf_token', decrypt=False)) == 30)

    def test_generates_token_every_request(self):
        self.middleware.every_request = True
        self.get('/test/10')
        self.middleware = self.container.resolve(self.middleware)
        token1 = self.middleware.verify_token()
        token2 = self.middleware.verify_token()

        self.assertEqual(len(token1), 30)
        self.assertEqual(len(token2), 30)
        self.assertNotEqual(token1, token2)

    def test_does_not_generate_token_every_request(self):
        self.middleware.every_request = False
        self.get('/test/10')
        self.middleware = self.container.resolve(self.middleware)
        token1 = self.middleware.verify_token()
        token2 = self.middleware.verify_token()

        self.assertEqual(len(token1), 30)
        self.assertEqual(len(token2), 30)
        self.assertEqual(token1, token2)
