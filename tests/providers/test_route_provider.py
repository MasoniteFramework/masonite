import unittest

from app.http.controllers.ControllerTest import ControllerTest
from config import application, middleware
from masonite.app import App
from masonite.auth import Csrf
from masonite.providers.RouteProvider import RouteProvider
from masonite.request import Request
from masonite.response import Response
from masonite.routes import Get, Match, Route
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.view import View
from masonite.auth import Auth
from masonite.managers import AuthManager
from masonite.drivers import AuthCookieDriver
from masonite.testing import TestCase
from masonite.exceptions import RouteNotFoundException


class TestRouteProvider(TestCase):

    def setUp(self):
        super().setUp()
        # self.app = App()
        # self.app.bind('Container', self.app)
        # self.app.bind('Environ', generate_wsgi())
        # self.app.bind('Application', application)
        # self.app.bind('WebRoutes', [])
        # self.app.bind('Route', Route(self.app.make('Environ')))
        # self.app.bind('Request', Request(
        #     self.app.make('Environ')).load_app(self.app))
        # self.app.simple(Response(self.app))
        # self.app.bind('StatusCode', None)
        # self.app.bind('HttpMiddleware', middleware.HTTP_MIDDLEWARE)
        # view = View(self.app)
        # self.app.bind('ViewClass', view)
        # self.app.bind('View', view.render)
        # self.app.bind('Auth', Auth)
        # self.app.bind('Csrf', Csrf(self.app.make('Request')))
        # self.app.bind('AuthCookieDriver', AuthCookieDriver)
        # self.app.bind('AuthManager', AuthManager(self.app).driver('cookie'))
        # self.provider = RouteProvider()
        # self.provider.app = self.app

    def test_controller_that_returns_a_view(self):
        self.routes(only=[Get('/view', ControllerTest.test), Get('/view/', ControllerTest.test)])

        self.assertTrue(self.get('/view').contains('test'))
        self.assertTrue(self.get('/view/').contains('test'))

    def test_home_route(self):
        self.routes(only=[Get('/', ControllerTest.test)])
        self.assertTrue(self.get('/').contains('test'))

    def test_base_route_can_set_request_params(self):
        self.routes(only=[Get('/@id', ControllerTest.test)])
        self.get('/test').assertParameterEquals('id', 'test')

    def test_no_base_route_returns_404(self):
        self.routes(only=[Get('/', ControllerTest.test)])

        with self.assertRaises(RouteNotFoundException):
            self.assertIsNone(self.get('/test'))

    def test_controller_that_return_a_view_with_trailing_slash(self):
        self.routes(only=[Get('/view', ControllerTest.test)])
        self.assertTrue(self.get('/view/').contains('test'))

    def test_match_route_returns_controller(self):
        self.routes(only=[Match(['GET', 'POST']).route('/view', ControllerTest.returns_a_view)])

        self.assertTrue(self.get('/view').contains('hey'))

    def test_provider_runs_through_routes(self):
        self.routes(only=[Get('/test', ControllerTest.test)])

        self.assertTrue(self.get('/test').headerIs('Content-Type', 'text/html; charset=utf-8'))

    def test_sets_request_params(self):
        self.routes(only=[Get('/test/@id', ControllerTest.test)])

        self.assertTrue(self.get('/test/1').parameterIs('id', '1'))

    def test_can_use_resolving_params(self):
        self.routes(only=[Get('/test/@id', ControllerTest.get_param)])

        self.assertEqual(self.get('/test/1').container.make('Request').first, '1')

    def test_can_use_resolving_params_and_object(self):
        self.routes(only=[Get('/test/@id', ControllerTest.get_param_and_object)])

        self.assertEqual(self.get('/test/1').container.make('Request').first, '1')

    def test_url_with_dots_finds_route(self):
        
        self.routes(only=[Get('/test/@endpoint', ControllerTest.test)])

        self.assertTrue(self.get('/test/user.endpoint').parameterIs('endpoint', 'user.endpoint'))

    def test_view_returns_with_route_view(self):
        self.routes(only=[Get().view('/test/route', 'test', {'test': 'testing'})])

        self.assertTrue(self.get('/test/route').contains('testing'))

    def test_url_with_dashes_finds_route(self):

        self.routes(only=[Get('/test/@endpoint', ControllerTest.test)])
        self.assertEqual(self.get('/test/user-endpoint').container.make('Request').param('endpoint'), 'user-endpoint')

        # self.app.bind(
        #     'WebRoutes', [Get('/test/@endpoint', ControllerTest.test)])

        # self.provider.boot(
        #     self.app.make('Route'),
        #     self.app.make('Request'),
        #     self.app.make(Response)
        # )

        

        # self.assertEqual(self.app.make('Request').param('endpoint'), 'user-endpoint')

    def test_param_returns_param(self):
        self.routes(only=[Get('/test/@id', ControllerTest.param)])
        self.assertTrue(self.get('/test/1').contains('1'))

    def test_custom_route_compiler_returns_param(self):
        self.routes(only=[Get('/test/@id:signed', ControllerTest.param)])
        self.assertTrue(self.get('/test/1').contains('1'))

    def test_route_subdomain_ignores_routes(self):
        self.routes(only=[Get('/view', ControllerTest.test)])
        
        with self.assertRaises(RouteNotFoundException):
            self.withSubdomains().get('/view', wsgi={
                'HTTP_HOST': 'subb.domain.com'
            }).assertIsStatus(404)


    def test_controller_returns_json_response_for_dict(self):
        self.routes(only=[Get('/view', ControllerTest.returns_a_dict)])

        self.assertTrue(
            self.get('/view').headerIs('Content-Type', 'application/json; charset=utf-8')
        )

    def test_route_runs_str_middleware(self):
        self.routes(only=[Get('/view', ControllerTest.returns_a_dict).middleware('test')])
        self.assertEqual(self.get('/view').container.make('Request').path, 'test/middleware/before/ran')

    def test_route_runs_middleware_with_list(self):
        self.routes(only=[Get('/view', ControllerTest.returns_a_dict).middleware('middleware.test')])
        
        request = self.get('/view').container.make('Request')

        self.assertEqual(request.path, 'test/middleware/before/ran')
        self.assertTrue(request.attribute)


class Middleware:

    def before(self):
        pass

    def after(self):
        pass
