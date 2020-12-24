
import unittest

from app.http.controllers.subdirectory.SubController import SubController
from app.http.controllers.subdirectory.deep.DeepController import DeepController
from src.masonite.app import App
from src.masonite.exceptions import (InvalidRouteCompileException,
                                     RouteException)
from src.masonite.helpers.routes import create_matchurl, flatten_routes, group
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.routes import (Connect, Delete, Get, Head, Match, Options,
                                 Patch, Post, Put, Resource, Redirect, Route, RouteGroup,
                                 Trace)
from src.masonite.testing import TestCase, generate_wsgi
from src.masonite.exceptions import RouteNotFoundException

class TestRoutes(TestCase):

    def setUp(self):
        super().setUp()
        self.route = Route(generate_wsgi())

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
        self.assertEqual(Get('some/url', 'TestController@show').route_url, '/some/url')

    def test_route_is_not_post(self):
        self.assertEqual(self.route.is_post(), False)

    def test_route_is_post(self):
        self.route.environ['REQUEST_METHOD'] = 'POST'
        self.assertEqual(self.route.is_post(), True)

    def test_compile_route_to_regex(self):
        get_route = Get('test/route', '')
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/route\/$')

        get_route = Get('test/@route', '')
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/([\w.-]+)\/$')

        get_route = Get('test/@route:int', '')
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/(\d+)\/$')

        get_route = Get('test/@route:string', '')
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/([a-zA-Z]+)\/$')

    def test_route_can_add_compilers(self):
        get_route = Get('test/@route:int', 'None')
        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/(\d+)\/$')

        self.route.compile('year', r'[0-9]{4}')

        get_route = Get('test/@route:year', '')

        self.assertEqual(get_route.compile_route_to_regex(), r'^\/test\/[0-9]{4}\/$')

        with self.assertRaises(InvalidRouteCompileException):
            get_route = Get().route('test/@route:none', None)
            get_route.request = self.container.make('Request')
            create_matchurl('/test/1', get_route)

    def test_route_can_add_compilers_inside_route_group(self):
        self.route.compile('year', r'[0-9]{4}')
        group = RouteGroup([
            Get().route('/@route:year', 'TestController@show')
        ], prefix="/test")

        self.assertEqual(group[0].compile_route_to_regex(), r'^\/test\/[0-9]{4}\/$')

        with self.assertRaises(InvalidRouteCompileException):
            get_route = Get().route('test/@route:none', None)
            get_route.request = self.container.make('Request')
            create_matchurl('/test/1', get_route)

    def test_route_gets_controllers(self):
        self.assertTrue(Get('test/url', 'TestController@show'))
        self.assertTrue(Get('test/url', '/app.http.test_controllers.TestController@show'))

    def test_route_doesnt_break_on_incorrect_controller(self):
        self.assertTrue(Get('test/url', 'BreakController@show'))


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
            Get('/test/1', 'TestController@show'),
            Get('/test/2', 'TestController@show')
        ])

        self.assertEqual(routes[0].route_url, '/example/test/1')
        self.assertEqual(routes[1].route_url, '/example/test/2')

    def test_group_route_sets_middleware(self):
        routes = RouteGroup([
            Get('/test/1', 'TestController@show').middleware('another'),
            Get('/test/2', 'TestController@show'),
            RouteGroup([
                Get('/test/3', 'TestController@show'),
                Get('/test/4', 'TestController@show')
            ], middleware=('test', 'test2'))
        ], middleware=('auth', 'user'))

        self.assertIsInstance(routes, list)
        self.assertEqual(['another', 'auth', 'user'], routes[0].list_middleware)
        self.assertEqual(['auth', 'user'], routes[1].list_middleware)
        self.assertEqual(['test', 'test2', 'auth', 'user'], routes[2].list_middleware)

    def test_group_route_namespace(self):
        routes = RouteGroup([
            Get('/test/1', 'SubController@show'),
        ], namespace='subdirectory.')

        self.assertIsInstance(routes, list)
        self.assertEqual(SubController, routes[0].controller)

    def test_group_route_namespace_deep(self):
        routes = RouteGroup([
            RouteGroup([
                Get('/test/1', 'DeepController@show'),
            ], namespace='deep.')
        ], namespace='subdirectory.')

        self.assertIsInstance(routes, list)
        self.assertEqual(DeepController, routes[0].controller)

    def test_group_route_namespace_deep_using_route_values_in_constructor(self):
        routes = RouteGroup([
            RouteGroup([
                Get('/test/1', 'DeepController@show'),
            ], namespace='deep.')
        ], namespace='subdirectory.')

        self.assertIsInstance(routes, list)
        self.assertEqual(DeepController, routes[0].controller)

    def test_group_route_namespace_deep_no_dots(self):
        routes = RouteGroup([
            RouteGroup([
                Get().route('/test/1', 'DeepController@show'),
            ], namespace='deep')
        ], namespace='subdirectory')

        self.assertIsInstance(routes, list)
        self.assertEqual(DeepController, routes[0].controller)

    def test_group_route_sets_domain(self):
        routes = RouteGroup([
            Get('/test/1', 'TestController@show'),
            Get('/test/2', 'TestController@show')
        ], domain=['www'])

        self.assertEqual(routes[0].required_domain, ['www'])

    def test_group_adds_methods(self):
        routes = RouteGroup([
            Get('/test/1', 'TestController@show'),
            Get('/test/2', 'TestController@show')
        ], add_methods=['OPTIONS'])

        self.assertEqual(routes[0].method_type, ['GET', 'OPTIONS'])

    def test_group_route_sets_prefix(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get('/test/2', 'TestController@show')
        ], prefix='/dashboard')

        self.assertEqual(routes[0].route_url, '/dashboard/test/1')

    def test_group_route_sets_prefix_no_route(self):
        routes = RouteGroup([
            Get('', 'TestController@show'),
        ], prefix='/dashboard')

        self.assertEqual(routes[0].route_url, '/dashboard')

    def test_group_route_sets_name(self):
        RouteGroup([
            Get('/test/1', 'TestController@show').name('create'),
            Get('/test/2', 'TestController@show').name('edit')
        ], name='post.')

    def test_group_route_sets_name_for_none_route(self):
        routes = RouteGroup([
            Get('/test/1', 'TestController@show').name('create'),
            Get('/test/2', 'TestController@show')
        ], name='post.')

        self.assertEqual(routes[0].named_route, 'post.create')
        self.assertEqual(routes[1].named_route, None)

    def test_flatten_flattens_multiple_lists(self):
        routes = [
            Get('/test/1', 'TestController@show').name('create'),
            RouteGroup([
                Get('/test/1', 'TestController@show').name('create'),
                Get('/test/2', 'TestController@show').name('edit'),
                RouteGroup([
                    Get('/test/1', 'TestController@show').name('update'),
                    Get('/test/2', 'TestController@show').name('delete'),
                    RouteGroup([
                        Get('/test/3', 'TestController@show').name('update'),
                        Get('/test/4', 'TestController@show').name('delete'),
                    ], middleware=('auth')),
                ], name='post.')
            ], prefix='/dashboard')
        ]

        routes = flatten_routes(routes)

        self.assertEqual(routes[3].route_url, '/dashboard/test/1')
        self.assertEqual(routes[3].named_route, 'post.update')

    def test_redirect_route(self):
        route = Redirect('/test1', '/test2')
        # request = Request(generate_wsgi())
        request = self.container.make('Request')
        response = self.container.make(Response)
        route.load_request(request)
        request.load_app(self.container)

        route.get_response()
        self.assertTrue(response.is_status(302))
        self.assertEqual(request.redirect_url, '/test2')

    def test_redirect_can_use_301(self):
        request = self.container.make('Request')
        response = self.container.make(Response)
        route = Redirect('/test1', '/test3', status=301)

        route.load_request(request)
        request.load_app(self.container)
        route.get_response()
        self.assertTrue(response.is_status(301))
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

class TestRouteResources(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(only=[Resource('/user', 'UserResourceController', names={
            'create': 'users.build'
        })])

    def test_has_correct_controllers(self):
        self.get('/user').assertHasController('UserResourceController@index').assertIsNotNamed()
        self.get('/user/create').assertHasController('UserResourceController@create').assertIsNamed('users.build')
        self.post('/user').assertHasController('UserResourceController@store').assertIsNotNamed()
        self.get('/user/1').assertHasController('UserResourceController@show').assertIsNotNamed()
        self.get('/user/1/edit').assertHasController('UserResourceController@edit').assertIsNotNamed()
        self.put('/user/1').assertHasController('UserResourceController@update').assertIsNotNamed()
        self.delete('/user/1').assertHasController('UserResourceController@destroy').assertIsNotNamed()


class WsgiInputTestClass:

    def load(self, byte):
        self.byte = byte
        return self

    def read(self, _):
        return self.byte
