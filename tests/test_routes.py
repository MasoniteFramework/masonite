from masonite.routes import Route
from masonite.request import Request
from masonite.app import App
from masonite.routes import Get, Post, Put, Patch, Delete, RouteGroup, Match, Redirect
from masonite.helpers.routes import group, flatten_routes
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.exceptions import InvalidRouteCompileException, RouteException
from app.http.controllers.subdirectory.SubController import SubController
import pytest


class TestRoutes:

    def setup_method(self):
        self.route = Route(generate_wsgi())
        self.request = Request(generate_wsgi())

    def test_route_is_callable(self):
        assert callable(Get)
        assert callable(Post)
        assert callable(Put)
        assert callable(Patch)
        assert callable(Delete)

    def test_route_get_returns_output(self):
        assert self.route.get('url', 'output') == 'output'

    def test_route_is_not_post(self):
        assert self.route.is_post() == False

    def test_route_is_post(self):
        self.route.environ['REQUEST_METHOD'] = 'POST'
        assert self.route.is_post() == True

    def test_compile_route_to_regex(self):
        get_route = Get().route('test/route', None)
        assert get_route.compile_route_to_regex(self.route) == '^test\\/route\\/$'

        get_route = Get().route('test/@route', None)
        assert get_route.compile_route_to_regex(self.route) == '^test\\/([\\w.-]+)\\/$'

        get_route = Get().route('test/@route:int', None)
        assert get_route.compile_route_to_regex(self.route) == '^test\\/(\\d+)\\/$'

        get_route = Get().route('test/@route:string', None)
        assert get_route.compile_route_to_regex(self.route) == '^test\\/([a-zA-Z]+)\\/$'

    def test_route_can_add_compilers(self):
        get_route = Get().route('test/@route:int', None)
        assert get_route.compile_route_to_regex(self.route) == '^test\\/(\\d+)\\/$'

        self.route.compile('year', r'[0-9]{4}')

        get_route = Get().route('test/@route:year', None)

        assert get_route.compile_route_to_regex(self.route) == '^test\\/[0-9]{4}\\/$'

        get_route = Get().route('test/@route:slug', None)
        with pytest.raises(InvalidRouteCompileException):
            get_route.compile_route_to_regex(self.route)

    def test_route_gets_controllers(self):
        assert Get().route('test/url', 'TestController@show')
        assert Get().route('test/url', '/app.http.test_controllers.TestController@show')

    def test_route_doesnt_break_on_incorrect_controller(self):
        assert Get().route('test/url', 'BreakController@show')

    def test_route_gets_deeper_module_controller(self):
        route = Get().route('test/url', 'subdirectory.SubController@show')
        assert route.controller
        assert isinstance(route.controller, SubController.__class__)

    def test_route_can_have_multiple_routes(self):
        assert Match(['GET', 'POST']).route('test/url', 'TestController@show').method_type == ['GET', 'POST']

    def test_match_routes_convert_lowercase_to_uppercase(self):
        assert Match(['Get', 'Post']).route('test/url', 'TestController@show').method_type == ['GET', 'POST']

    def test_match_routes_raises_exception_with_non_list_method_types(self):
        with pytest.raises(RouteException):
            assert Match('get').route('test/url', 'TestController@show').method_type == ['GET', 'POST']

    def test_group_route(self):
        routes = group('/example', [
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ])

        assert routes[0].route_url == '/example/test/1'
        assert routes[1].route_url == '/example/test/2'

    def test_group_route_sets_middleware(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show').middleware('another'),
            Get().route('/test/2', 'TestController@show'),
            RouteGroup([
                Get().route('/test/3', 'TestController@show'),
                Get().route('/test/4', 'TestController@show')
            ], middleware=('test', 'test2'))
        ], middleware=('auth', 'user'))

        assert isinstance(routes, list)
        assert ['another', 'auth', 'user'] == routes[0].list_middleware
        assert ['auth', 'user'] == routes[1].list_middleware
        assert ['test', 'test2', 'auth', 'user'] == routes[2].list_middleware

    def test_group_route_sets_domain(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], domain=['www'])

        assert routes[0].required_domain == ['www']

    def test_group_adds_methods(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], add_methods=['OPTIONS'])

        assert routes[0].method_type == ['GET', 'OPTIONS']

    def test_group_route_sets_prefix(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], prefix='/dashboard')

        assert routes[0].route_url == '/dashboard/test/1'

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

        assert routes[0].named_route == 'post.create'
        assert routes[1].named_route == None

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

        assert routes[3].route_url == '/dashboard/test/1'
        assert routes[3].named_route == 'post.update'

    def test_correctly_parses_json_with_dictionary(self):
        environ = generate_wsgi()
        environ['CONTENT_TYPE'] = 'application/json'
        environ['REQUEST_METHOD'] = 'POST'
        environ['wsgi.input'] = WsgiInputTestClass().load(b'{\n    "conta_corrente": {\n        "ocultar": false,\n        "visao_geral": true,\n        "extrato": true\n    }\n}')
        route = Route(environ)
        assert route.environ['QUERY_STRING'] == {
            "conta_corrente": {
                "ocultar": False,
                "visao_geral": True,
                "extrato": True
            }
        }

    def test_correctly_parses_json_with_list(self):
        environ = generate_wsgi()
        environ['CONTENT_TYPE'] = 'application/json'
        environ['REQUEST_METHOD'] = 'POST'
        environ['wsgi.input'] = WsgiInputTestClass().load(b'{\n    "options": ["foo", "bar"]\n}')
        route = Route(environ)
        assert route.environ['QUERY_STRING'] == {
            "options": ["foo", "bar"]
        }
    
    def test_redirect_route(self):
        route = Redirect('/test1', '/test2')
        request = Request(generate_wsgi())
        route.load_request(request)
        request.load_app(App())

        route.get_response()
        assert request.is_status(302)
        assert request.redirect_url == '/test2'

    def test_redirect_can_use_301(self):
        request = Request(generate_wsgi())
        route = Redirect('/test1', '/test3', status=301)
        
        route.load_request(request)
        request.load_app(App())
        route.get_response()
        assert request.is_status(301)
        assert request.redirect_url == '/test3'

    def test_redirect_can_change_method_type(self):
        request = Request(generate_wsgi())
        route = Redirect('/test1', '/test3', methods=['POST', 'PUT'])
        assert route.method_type == ['POST', 'PUT']


class WsgiInputTestClass:

    def load(self, byte):
        self.byte = byte
        return self

    def read(self, request_body_size):
        return self.byte
