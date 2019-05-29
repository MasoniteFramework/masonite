import unittest

from app.http.controllers.ControllerTest import ControllerTest
from config import application, middleware
from masonite.app import App
from masonite.providers.RouteProvider import RouteProvider
from masonite.request import Request
from masonite.response import Response
from masonite.routes import Get, Match, Route
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.view import View


class TestRouteProvider(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Container', self.app)
        self.app.bind('Environ', generate_wsgi())
        self.app.bind('Application', application)
        self.app.bind('WebRoutes', [])
        self.app.bind('Route', Route(self.app.make('Environ')))
        self.app.bind('Request', Request(
            self.app.make('Environ')).load_app(self.app))
        self.app.simple(Response(self.app))
        self.app.bind('StatusCode', None)
        self.app.bind('HttpMiddleware', middleware.HTTP_MIDDLEWARE)
        view = View(self.app)
        self.app.bind('ViewClass', view)
        self.app.bind('View', view.render)
        self.provider = RouteProvider()
        self.provider.app = self.app

    def test_controller_that_returns_a_view(self):
        self.app.make('Route').url = '/view'
        self.app.bind('WebRoutes', [Get('/view', ControllerTest.test)])
        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), 'test')

        self.app.make('Route').url = '/view/'
        self.app.bind('WebRoutes', [Get('/view', ControllerTest.test)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        # self.assertEqual(self.app.make('Response'), 'test')

    def test_base_route_hits_controller(self):
        self.app.make('Route').url = '/test'
        self.app.bind('WebRoutes', [get('/@id', ControllerTest.test)])
        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        assert self.app.make('Request').param('id') == 'test'
        assert self.app.make('Response') == 'test'

    def test_controller_that_return_a_view_with_trailing_slash(self):

        self.app.make('Route').url = '/view/'
        self.app.bind('WebRoutes', [Get('/view/', ControllerTest.test)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), 'test')

        self.app.make('Route').url = '/view'
        self.app.bind('WebRoutes', [Get('/view/', ControllerTest.test)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), 'test')

    def test_match_route_returns_controller(self):
        self.app.make('Route').url = '/view'
        self.app.bind(
            'WebRoutes', [Match(['GET', 'POST']).route('/view', ControllerTest.returns_a_view)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), 'hey')

    def test_provider_runs_through_routes(self):
        self.app.make('Route').url = '/test'
        self.app.bind('WebRoutes', [Get('/test', ControllerTest.test)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').header(
            'Content-Type'), 'text/html; charset=utf-8')

    def test_sets_request_params(self):
        self.app.make('Route').url = '/test/1'
        self.app.bind('WebRoutes', [Get('/test/@id', ControllerTest.test)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').param('id'), '1')

    def test_can_use_resolving_params(self):
        self.app.make('Route').url = '/test/1'
        self.app.bind('WebRoutes', [Get('/test/@id', ControllerTest.get_param)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').first, '1')

    def test_can_use_resolving_params_and_object(self):
        self.app.make('Route').url = '/test/1'
        self.app.bind('WebRoutes', [Get('/test/@id', ControllerTest.get_param_and_object)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').first, '1')
        # self.assertEqual(isinstance(self.app.make('Request').view, View)

    def test_url_with_dots_finds_route(self):
        self.app.make('Route').url = '/test/user.endpoint'
        self.app.bind(
            'WebRoutes', [Get('/test/@endpoint', ControllerTest.test)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').param('endpoint'), 'user.endpoint')

    def test_view_returns_with_route_view(self):
        self.app.make('Route').url = '/test/route'
        self.app.bind('WebRoutes', [
            Get().view('/test/route', 'test', {'test': 'testing'})
        ])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), 'testing')

    def test_url_with_dashes_finds_route(self):
        self.app.make('Route').url = '/test/user-endpoint'
        self.app.bind(
            'WebRoutes', [Get('/test/@endpoint', ControllerTest.test)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').param('endpoint'), 'user-endpoint')

    def test_param_returns_param(self):
        self.app.make('Route').url = '/test/1'
        self.app.bind('WebRoutes', [Get('/test/@id', ControllerTest.param)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), '1')

    def test_custom_route_compiler_returns_param(self):
        self.app.make('Route').url = '/test/1'
        self.app.make('Route').compile('signed', r'([\w.-]+)')
        self.app.bind('WebRoutes', [Get('/test/@id:signed', ControllerTest.param)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), '1')

    def test_route_subdomain_ignores_routes(self):
        self.app.make('Route').url = '/test'
        self.app.make('Environ')['HTTP_HOST'] = 'subb.domain.com'
        self.app.bind('WebRoutes', [Get('/test', ControllerTest.test)])

        request = self.app.make('Request')
        request.activate_subdomains()

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Response'), 'Route not found. Error 404')

    def test_controller_returns_json_response_for_dict(self):
        self.app.make('Route').url = '/view'
        self.app.bind(
            'WebRoutes', [Get('/view', ControllerTest.returns_a_dict)])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').header(
            'Content-Type'), 'application/json; charset=utf-8')

    def test_route_runs_str_middleware(self):
        self.app.make('Route').url = '/view'
        self.app.bind('RouteMiddleware', middleware.ROUTE_MIDDLEWARE)
        self.app.bind('WebRoutes', [
            Get('/view', ControllerTest.returns_a_dict).middleware('test')
        ]
        )

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').path, 'test/middleware/before/ran')

    def test_route_runs_middleware_with_list(self):
        self.app.make('Route').url = '/view'
        self.app.bind('RouteMiddleware', middleware.ROUTE_MIDDLEWARE)
        self.app.bind('WebRoutes', [
            Get('/view', ControllerTest.returns_a_dict).middleware('middleware.test')
        ]
        )

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response)
        )

        self.assertEqual(self.app.make('Request').path, 'test/middleware/before/ran')
        self.assertEqual(self.app.make('Request').attribute, True)


class Middleware:

    def before(self):
        pass

    def after(self):
        pass
