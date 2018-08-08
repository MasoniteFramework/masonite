from masonite.app import App
from masonite.request import Request
from masonite.view import View
from masonite.routes import Get, Route
from masonite.testsuite import generate_wsgi
from masonite.auth import Csrf
from masonite.providers import RouteProvider
from app.http.middleware.TestMiddleware import TestMiddleware as MiddlewareTest
from app.http.middleware.TestHttpMiddleware import TestHttpMiddleware as MiddlewareHttpTest

class TestMiddleware:

    def setup_method(self):
        self.app = App()
        self.app.bind('Environ', generate_wsgi())
        self.app.make('Environ')
        self.app.bind('Headers', [])
        self.app.bind('Request', Request(self.app.make('Environ')).load_app(self.app))
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
            'test': MiddlewareTest
        })

        self.provider = RouteProvider()
        self.provider.app = self.app
    
    def test_route_middleware_runs(self):
        self.app.resolve(self.provider.boot)
        assert self.app.make('Request').path == '/test/middleware'

    def test_http_middleware_runs(self):
        self.app.resolve(self.provider.boot)
        assert self.app.make('Request').path == '/test/middleware'
        assert self.app.make('Request').environ['HTTP_TEST'] == 'test'


