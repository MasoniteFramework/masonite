
import unittest

from app.http.controllers.subdirectory.SubController import SubController
from src.masonite.app import App
from src.masonite.exceptions import (InvalidRouteCompileException,
                                     RouteException)
from src.masonite.helpers.routes import create_matchurl, flatten_routes, group
from src.masonite.request import Request
from src.masonite.routes import (Connect, Delete, Get, Head, Match, Options,
                                 Patch, Post, Put, Redirect, Route, RouteGroup,
                                 Trace)
from src.masonite.testing import TestCase
from src.masonite.testsuite.TestSuite import generate_wsgi
from src.masonite.exceptions import RouteNotFoundException

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.route = Route(generate_wsgi())
        self.request = Request(generate_wsgi())

    def test_route_is_callable(self):
        self.assertTrue(callable(Get))
        self.assertTrue(callable(Head))
        self.assertTrue(callable(Post))
        self.assertTrue(callable(Match))
        self.assertTrue(callable(Put))
        self.assertTrue(callable(Patch))
        self.assertTrue(callable(Delete))
        self.assertTrue(callable(Connect))
        self.assertTrue(callable(Options))
        self.assertTrue(callable(Trace))

    def test_route_prefixes_forward_slash(self):
        self.assertEqual(Get().route('some/url', 'TestController@show').route_url, '/some/url')

    def test_route_is_not_post(self):
        self.assertEqual(self.route.is_post(), False)

    def test_route_is_post(self):
        self.route.environ['REQUEST_METHOD'] = 'POST'
        self.assertEqual(self.route.is_post(), True)

    def test_compile_route_to_regex(self):
        get_route = Get().route('test/route', None)
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/route\/$')

        get_route = Get().route('test/@route', None)
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/([\w.-]+)\/$')

        get_route = Get().route('test/@route:int', None)
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/(\d+)\/$')

        get_route = Get().route('test/@route:string', None)
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/([a-zA-Z]+)\/$')

    def test_route_can_add_compilers(self):
        get_route = Get().route('test/@route:int', None)
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/(\d+)\/$')

        self.route.compile('year', r'[0-9]{4}')

        get_route = Get().route('test/@route:year', None)

        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/[0-9]{4}\/$')

        with self.assertRaises(InvalidRouteCompileException):
            get_route = Get().route('test/@route:none', None)
            create_matchurl('/test/1', get_route)

    def test_route_gets_controllers(self):
        self.assertTrue(Get().route('test/url', 'TestController@show'))
        self.assertTrue(Get().route('test/url', '/app.http.test_controllers.TestController@show'))

    def test_route_doesnt_break_on_incorrect_controller(self):
        self.assertTrue(Get().route('test/url', 'BreakController@show'))

    def test_route_can_pass_route_values_in_constructor(self):
        route = Get('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Head('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Post('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Put('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Patch('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Delete('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Connect('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Options('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')
        route = Trace('test/url', 'BreakController@show')
        self.assertEqual(route.route_url, '/test/url')

    def test_route_can_pass_route_values_in_constructor_and_use_middleware(self):
        route = Get('test/url', 'BreakController@show').middleware('auth')
        self.assertEqual(route.route_url, '/test/url')
        self.assertEqual(route.list_middleware, ['auth'])

    def test_route_gets_deeper_module_controller(self):
        route = Get().route('test/url', 'subdirectory.SubController@show')
        self.assertTrue(route.controller)
        self.assertIsInstance(route.controller, SubController.__class__)

    def test_route_can_have_multiple_routes(self):
        self.assertEqual(Match(['GET', 'POST']).route('test/url', 'TestController@show').method_type, ['GET', 'POST'])

    def test_match_routes_convert_lowercase_to_uppercase(self):
        self.assertEqual(Match(['Get', 'Post']).route('test/url', 'TestController@show').method_type, ['GET', 'POST'])

    def test_match_routes_raises_exception_with_non_list_method_types(self):
        with self.assertRaises(RouteException):
            self.assertEqual(Match('get').route('test/url', 'TestController@show').method_type, ['GET', 'POST'])

    def test_group_route(self):
        routes = group('/example', [
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ])

        self.assertEqual(routes[0].route_url, '/example/test/1')
        self.assertEqual(routes[1].route_url, '/example/test/2')

    def test_group_route_sets_middleware(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show').middleware('another'),
            Get().route('/test/2', 'TestController@show'),
            RouteGroup([
                Get().route('/test/3', 'TestController@show'),
                Get().route('/test/4', 'TestController@show')
            ], middleware=('test', 'test2'))
        ], middleware=('auth', 'user'))

        self.assertIsInstance(routes, list)
        self.assertEqual(['another', 'auth', 'user'], routes[0].list_middleware)
        self.assertEqual(['auth', 'user'], routes[1].list_middleware)
        self.assertEqual(['test', 'test2', 'auth', 'user'], routes[2].list_middleware)

    def test_group_route_sets_domain(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], domain=['www'])

        self.assertEqual(routes[0].required_domain, ['www'])

    def test_group_adds_methods(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], add_methods=['OPTIONS'])

        self.assertEqual(routes[0].method_type, ['GET', 'OPTIONS'])

    def test_group_route_sets_prefix(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], prefix='/dashboard')

        self.assertEqual(routes[0].route_url, '/dashboard/test/1')

    def test_group_route_sets_prefix_no_route(self):
        routes = RouteGroup([
            Get('', 'TestController@show'),
        ], prefix='/dashboard')

        self.assertEqual(routes[0].route_url, '/dashboard')

    def test_group_route_sets_name(self):
        RouteGroup([
            Get().route('/test/1', 'TestController@show').name('create'),
            Get().route('/test/2', 'TestController@show').name('edit')
        ], name='post.')

    def test_group_route_sets_name_for_none_route(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show').name('create'),
            Get().route('/test/2', 'TestController@show')
        ], name='post.')

        self.assertEqual(routes[0].named_route, 'post.create')
        self.assertEqual(routes[1].named_route, None)

    def test_flatten_flattens_multiple_lists(self):
        routes = [
            Get().route('/test/1', 'TestController@show').name('create'),
            RouteGroup([
                Get().route('/test/1', 'TestController@show').name('create'),
                Get().route('/test/2', 'TestController@show').name('edit'),
                RouteGroup([
                    Get().route('/test/1', 'TestController@show').name('update'),
                    Get().route('/test/2', 'TestController@show').name('delete'),
                    RouteGroup([
                        Get().route('/test/3', 'TestController@show').name('update'),
                        Get().route('/test/4', 'TestController@show').name('delete'),
                    ], middleware=('auth')),
                ], name='post.')
            ], prefix='/dashboard')
        ]

        routes = flatten_routes(routes)

        self.assertEqual(routes[3].route_url, '/dashboard/test/1')
        self.assertEqual(routes[3].named_route, 'post.update')

    def test_correctly_parses_json_with_dictionary(self):
        environ = generate_wsgi()
        environ['CONTENT_TYPE'] = 'application/json'
        environ['REQUEST_METHOD'] = 'POST'
        environ['wsgi.input'] = WsgiInputTestClass().load(b'{\n    "conta_corrente": {\n        "ocultar": false,\n        "visao_geral": true,\n        "extrato": true\n    }\n}')
        route = Route(environ)
        self.assertEqual(route.environ['QUERY_STRING'], {
            "conta_corrente": {
                "ocultar": False,
                "visao_geral": True,
                "extrato": True
            }
        })

    def test_correctly_parses_json_with_list(self):
        environ = generate_wsgi()
        environ['CONTENT_TYPE'] = 'application/json'
        environ['REQUEST_METHOD'] = 'POST'
        environ['wsgi.input'] = WsgiInputTestClass().load(b'{\n    "options": ["foo", "bar"]\n}')
        route = Route(environ)
        self.assertEqual(route.environ['QUERY_STRING'], {
            "options": ["foo", "bar"]
        })

    def test_redirect_route(self):
        route = Redirect('/test1', '/test2')
        request = Request(generate_wsgi())
        route.load_request(request)
        request.load_app(App())

        route.get_response()
        self.assertTrue(request.is_status(302))
        self.assertEqual(request.redirect_url, '/test2')

    def test_redirect_can_use_301(self):
        request = Request(generate_wsgi())
        route = Redirect('/test1', '/test3', status=301)

        route.load_request(request)
        request.load_app(App())
        route.get_response()
        self.assertTrue(request.is_status(301))
        self.assertEqual(request.redirect_url, '/test3')

    def test_redirect_can_change_method_type(self):
        route = Redirect('/test1', '/test3', methods=['POST', 'PUT'])
        self.assertEqual(route.method_type, ['POST', 'PUT'])


class TestOptionalRoutes(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(only=[
            Get('/user/?name', 'TestController@v').name('user.name'),
            Get('/multiple/user/?name/?last', 'TestController@v').name('user.multiple'),
            Get('/default/user/?name', 'TestController@v').default({'name': 'Joseph'}),
            Get('/back/user/name?', 'TestController@v'),
            Get('/back/default/user/?name', 'TestController@v').default({'name': 'Joseph'}),
            Get('/optional/?name:int', 'TestController@v'),
        ])
    
    def test_can_get_name(self):
        self.get('/user/john').assertParameterIs('name', 'john')
        self.get('/user').assertParameterIs('name', None)
        self.get('/default/user/Bill').assertParameterIs('name', 'Bill')
        self.get('/default/user').assertParameterIs('name', 'Joseph')

    def test_can_get_optional_when_optional_is_in_back(self):
        self.get('/back/user/john').assertParameterIs('name', 'john')
        self.get('/back/user').assertParameterIs('name', None)
        self.get('/back/default/user/Bill').assertParameterIs('name', 'Bill')
        self.get('/back/default/user').assertParameterIs('name', 'Joseph')

    def test_can_get_optional_route_compilers(self):
        self.get('/optional/1').assertParameterIs('name', '1')

        with self.assertRaises(RouteNotFoundException):
            self.get('/optional/Joe')
        
        self.get('/optional').assertParameterIs('name', None)

    def test_cannot_get_longer_optional_parameter(self):
        with self.assertRaises(RouteNotFoundException):
            self.get('/user/john/settings').assertParameterIs('name', 'john')

    def test_route_helper_works(self):
        request = self.get('/user/john').request
        self.assertEqual(request.route('user.name'), '/user')
        self.assertEqual(request.route('user.name', {'name': 'john'}), '/user/john')
        self.assertEqual(request.route('user.multiple'), '/multiple/user')
        self.assertEqual(request.route('user.multiple', {'name': 'john'}), '/multiple/user/john')
        self.assertEqual(request.route('user.multiple', {'name': 'john', 'last': 'smith'}), '/multiple/user/john/smith')
        self.assertEqual(request.route('user.multiple', {'last': 'smith'}), '/multiple/user/smith')

class WsgiInputTestClass:

    def load(self, byte):
        self.byte = byte
        return self

    def read(self, _):
        return self.byte
