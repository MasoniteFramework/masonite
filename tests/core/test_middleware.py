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


class MiddlewareValueTest:

    def __init__(self, request: Request):
        self.request = request

    def before(self, value1, value2):
        self.request.value1 = value1
        self.request.value2 = value2


class TestMiddleware(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Environ', generate_wsgi())
        self.app.make('Environ')
        self.app.bind('StatusCode', None)
        self.app.bind('Request', Request(self.app.make('Environ')).load_app(self.app))
        self.app.simple(Response(self.app))
        self.app.bind('Csrf', Csrf(self.app.make('Request')))
        self.app.bind('Route', Route(self.app.make('Environ')))

        self.app.bind('ViewClass', View(self.app))

        self.app.bind('WebRoutes', [
            Get().route('/', 'TestController@show').middleware('test')
        ])

        self.app.bind('HttpMiddleware', [
            MiddlewareHttpTest
        ])

        self.app.bind('RouteMiddleware', {
            'test': MiddlewareTest,
            'throttle:1,2': MiddlewareValueTest
        })

        self.provider = RouteProvider()
        self.provider.app = self.app

    def test_route_middleware_runs(self):
        self.app.resolve(self.provider.boot)
        self.assertEqual(self.app.make('Request').path, '/test/middleware')

    def test_http_middleware_runs(self):
        self.app.resolve(self.provider.boot)
        self.assertEqual(self.app.make('Request').path, '/test/middleware')
        self.assertEqual(self.app.make('Request').environ['HTTP_TEST'], 'test')

    def test_route_middleware_can_pass_values(self):
        route = self.app.make('WebRoutes')[0]
        route.request = self.app.make('Request')
        route.list_middleware = ['throttle:1,2']
        route.run_middleware('before')
        self.assertEqual(route.request.value1, '1')
        self.assertEqual(route.request.value2, '2')
