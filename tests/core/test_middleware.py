from masonite.app import App
from masonite.request import Request
from masonite.response import Response
from masonite.view import View
from masonite.routes import Get, Route
from masonite.testsuite import generate_wsgi
from masonite.auth import Csrf
from masonite.providers import RouteProvider
from app.http.middleware.TestMiddleware import TestMiddleware as MiddlewareTest
from app.http.middleware.TestHttpMiddleware import TestHttpMiddleware as MiddlewareHttpTest
from config import application
import unittest
from masonite.testing import TestCase


class MiddlewareValueTest:

    def __init__(self, request: Request):
        self.request = request

    def before(self, value1, value2):
        self.request.value1 = value1
        self.request.value2 = value2


class TestMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(only=[
            Get().route('/', 'TestController@show').middleware('test'),
            Get().route('/test', 'TestController@show').middleware('throttle:1,2')
        ])

        self.withRouteMiddleware({
            'test': MiddlewareTest,
            'throttle': MiddlewareValueTest
        }).withHttpMiddleware([MiddlewareHttpTest])

    def test_route_middleware_runs(self):
        self.assertEqual(self.get('/').container.make('Request').path, '/test/middleware')

    def test_http_middleware_runs(self):
        self.assertEqual(self.get('/').container.make('Request').path, '/test/middleware')
        self.assertEqual(self.get('/').container.make('Request').environ['HTTP_TEST'], 'test')

    def test_route_middleware_can_pass_values(self):
        self.assertTrue(self.get('/test').container.make('Request').value1, '1')
        self.assertTrue(self.get('/test').container.make('Request').value2, '2')
