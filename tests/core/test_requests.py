import unittest
from cgi import MiniFieldStorage

import pytest

from app.http.test_controllers.TestController import TestController
from src.masonite.app import App
from src.masonite.exceptions import InvalidHTTPStatusCode, RouteException
from src.masonite.helpers import config
from src.masonite.helpers.routes import flatten_routes
from src.masonite.helpers.time import cookie_expire_time
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.routes import Get, RouteGroup
from src.masonite.testing import generate_wsgi

WEB_ROUTES = flatten_routes([
    Get('/test', 'Controller@show').name('test'),
    RouteGroup([
        Get('/account', 'Controller@show').name('a_account'),
    ], prefix='/a')
])

wsgi_request = generate_wsgi()


class TestRequest(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.request = Request(wsgi_request).key(
            'NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY=').load_app(self.app)
        self.app.bind('Request', self.request)
        self.response = Response(self.app)
        self.app.simple(Response)

    def test_request_is_callable(self):
        """ Request should be callable """
        self.assertIsInstance(self.request, object)

    def test_request_input_should_return_input_on_get_request(self):
        self.assertEqual(self.request.input('application'), 'Masonite')
        self.assertEqual(self.request.input('application', 'foo'), 'Masonite')

    def test_request_input_should_return_default_when_not_exists(self):
        self.assertEqual(self.request.input('foo', 'bar'), 'bar')

    def test_request_all_should_return_params(self):
        self.assertEqual(self.request.all(), {'application': 'Masonite'})

    def test_request_all_without_internal_request_variables(self):
        self.request.request_variables.update({'__token': 'testing', 'application': 'Masonite'})
        self.assertEqual(self.request.all(), {'__token': 'testing', 'application': 'Masonite'})
        self.assertEqual(self.request.all(internal_variables=False), {'application': 'Masonite'})

    def test_request_has_should_return_bool(self):
        self.assertEqual(self.request.has('application'), True)
        self.assertEqual(self.request.has('shouldreturnfalse'), False)

    def test_request_has_should_accept_multiple_values(self):
        self.request.request_variables.update({'__token': 'testing', 'application': 'Masonite'})
        self.assertEqual(self.request.has('application'), True)
        self.assertEqual(self.request.has('shouldreturnfalse'), False)
        self.assertEqual(self.request.has('__token'), True)
        self.assertEqual(self.request.has('__token', 'shouldreturnfalse'), False)
        self.assertEqual(self.request.has('__token', 'application'), True)
        self.assertEqual(self.request.has('__token', 'application', 'shouldreturnfalse'), False)

    def test_request_set_params_should_return_self(self):
        self.assertEqual(self.request.set_params({'value': 'new'}), self.request)
        self.assertEqual(self.request.url_params, {'value': 'new'})

    def test_request_param_returns_parameter_set_or_false(self):
        self.request.set_params({'value': 'new'})
        self.assertEqual(self.request.param('value'), 'new')
        self.assertEqual(self.request.param('nullvalue'), False)

    def test_request_appends_cookie(self):
        self.assertEqual(self.request.cookie('appendcookie', 'value'), self.request)
        assert 'appendcookie' in self.request.environ['HTTP_COOKIE']

    def test_request_input_can_get_dictionary_elements(self):
        self.request.request_variables = {
            "user": {
                "address": [
                    {"id": 1, 'street': 'A Street'},
                    {"id": 2, 'street': 'B Street'}
                ]
            }
        }
        self.assertEqual(self.request.input('user.address.*.id'), [1, 2])
        self.assertEqual(self.request.input('user.address.*.street'), ['A Street', 'B Street'])
    
    def test_request_input_parses_query_string(self):
        query_string = "filter=name"
        self.request._set_standardized_request_variables(query_string)
        self.request._set_standardized_request_variables(query_string)
        self.assertEqual(self.request.input('filter'), 'name')

        query_string = "filter=name&user=Joe"
        self.request._set_standardized_request_variables(query_string)
        self.assertEqual(self.request.input('filter'), 'name')
        self.assertEqual(self.request.input('user'), 'Joe')

        query_string = "filter[name]=Joe&filter[email]=user@email.com"
        self.request._set_standardized_request_variables(query_string)
        self.assertEqual(self.request.input('filter')['name'], 'Joe')
        self.assertEqual(self.request.input('filter.name'), 'Joe')
        self.assertEqual(self.request.input('filter')['email'], 'user@email.com')
        self.assertEqual(self.request.input('filter.email'), 'user@email.com')

    def test_request_sets_and_gets_cookies(self):
        self.request.cookie('setcookie', 'value')
        self.assertEqual(self.request.get_cookie('setcookie'), 'value')

    def test_request_sets_expiration_cookie_2_months(self):
        self.request.cookies = []
        self.request.cookie('setcookie_expiration', 'value', expires='2 months')

        time = cookie_expire_time('2 months')

        self.assertEqual(self.request.get_cookie('setcookie_expiration'), 'value')
        self.assertEqual(self.request.get_raw_cookie('setcookie_expiration')['expires'], time)

    def test_delete_cookie(self):
        self.request.cookies = []
        self.request.cookie('delete_cookie', 'value')

        self.assertEqual(self.request.get_cookie('delete_cookie'), 'value')
        self.request.delete_cookie('delete_cookie')
        self.assertFalse(self.request.get_cookie('delete_cookie'))

    def test_delete_cookie_with_wrong_key(self):
        self.request.cookies = []
        self.request.cookie('cookie', 'value')
        self.request.key('wrongkey_TXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY=')
        self.assertIsNone(self.request.get_cookie('cookie'))

    def test_redirect_returns_request(self):
        self.assertEqual(self.request.redirect('newurl'), self.request)
        self.assertEqual(self.request.redirect_url, '/newurl')

    def test_request_no_input_returns_false(self):
        self.assertEqual(self.request.input('notavailable'), False)

    def test_request_mini_field_storage_returns_single_value(self):
        storages = {'test': [MiniFieldStorage('key', '1')]}
        self.request._set_standardized_request_variables(storages)
        self.assertEqual(self.request.input('test'), '1')

    def test_request_can_get_string_value(self):
        storages = {'test': 'value'}
        self.request._set_standardized_request_variables(storages)
        self.assertEqual(self.request.input('test'), 'value')

    def test_request_can_get_list_value(self):
        storages = {'test': ['foo', 'bar']}
        self.request._set_standardized_request_variables(storages)
        self.assertEqual(self.request.input('test'), ['foo', 'bar'])

    def test_request_mini_field_storage_doesnt_return_brackets(self):
        storages = {'test[]': [MiniFieldStorage('key', '1')]}
        self.request._set_standardized_request_variables(storages)
        self.assertEqual(self.request.input('test'), '1')

    def test_request_mini_field_storage_index(self):
        storages = {'test[index]': [MiniFieldStorage('key', '1')]}
        self.request._set_standardized_request_variables(storages)
        self.assertEqual(self.request.input('test[index]'), '1')

    def test_request_mini_field_storage_with_dot_notation(self):
        storages = {'test[index]': [MiniFieldStorage('key', '1')]}
        self.request._set_standardized_request_variables(storages)
        self.assertEqual(self.request.input('test.index'), '1')

    def test_request_mini_field_storage_returns_a_list(self):
        storages = {'test': [MiniFieldStorage(
            'key', '1'), MiniFieldStorage('key', '2')]}
        self.request._set_standardized_request_variables(storages)
        self.assertEqual(self.request.input('test'), ['1', '2'])

    def test_request_get_cookies_returns_cookies(self):
        self.assertEqual(self.request.get_cookies(), self.request.cookies)

    def test_request_set_user_sets_object(self):
        self.assertEqual(self.request.set_user(object), self.request)
        self.assertEqual(self.request.user_model, object)
        self.assertEqual(self.request.user(), object)

    def test_request_loads_app(self):
        app = App()
        app.bind('Request', self.request)
        app.make('Request').load_app(app)

        self.assertEqual(self.request.app(), app)
        self.assertEqual(app.make('Request').app(), app)

    def test_request_gets_input_from_container(self):
        container = App()
        container.bind('WSGI', object)
        container.bind('Environ', wsgi_request)

        for provider in config('providers.providers'):
            provider().load_app(container).register()

        container.bind('Response', 'test')
        container.bind('WebRoutes', [
            Get().route('url', 'TestController@show'),
            Get().route('url/', 'TestController@show'),
            Get().route('url/@firstname', 'TestController@show'),
        ])

        container.bind('Response', 'Route not found. Error 404')

        for provider in config('providers.providers'):
            located_provider = provider().load_app(container)

            container.resolve(located_provider.boot)

        self.assertEqual(container.make('Request').input('application'), 'Masonite')
        self.assertEqual(container.make('Request').all(), {'application': 'Masonite'})
        container.make('Request').environ['REQUEST_METHOD'] = 'POST'
        self.assertEqual(container.make('Request').environ['REQUEST_METHOD'], 'POST')
        self.assertEqual(container.make('Request').input('application'), 'Masonite')

    def test_redirections_reset(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', WEB_ROUTES)
        request = app.make('Request').load_app(app)

        request.redirect('test')

        self.assertEqual(request.redirect_url, '/test')

        request.reset_redirections()

        self.assertFalse(request.redirect_url)

        request.redirect_to('test')

        self.assertEqual(request.redirect_url, '/test')

        request.reset_redirections()

        self.assertFalse(request.redirect_url)

    def test_redirect_to_throws_exception_when_no_routes_found(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', WEB_ROUTES)
        request = app.make('Request').load_app(app)

        request.redirect_to('test')
        request.redirect(name='test')

        with pytest.raises(RouteException):
            request.redirect_to('notavailable')

        with pytest.raises(RouteException):
            request.redirect(name='notavailable')

    def test_request_has_subdomain_returns_bool(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        self.assertFalse(request.has_subdomain())
        self.assertIsNone(request.subdomain)

        request.environ['HTTP_HOST'] = 'test.localhost.com'

        request.header('TEST', 'set_this')
        self.assertEqual(request.header('TEST'), 'set_this')

        request.header('TEST', 'set_this', http_prefix=True)
        self.assertEqual(request.header('HTTP_TEST'), 'set_this')

    def test_redirect_compiles_url(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = '/test/url'

        self.assertEqual(request.compile_route_to_url(route), '/test/url')

    def test_redirect_compiles_url_with_1_slash(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = '/'

        self.assertEqual(request.compile_route_to_url(route), '/')

    def test_request_route_returns_url(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', [
            Get('/test/url', 'TestController@show').name('test.url'),
            Get('/test/url/@id', 'TestController@show').name('test.id')
        ])
        request = app.make('Request').load_app(app)

        self.assertEqual(request.route('test.url'), '/test/url')
        self.assertEqual(request.route('test.id', {'id': 1}), '/test/url/1')
        self.assertEqual(request.route('test.id', [1]), '/test/url/1')

        with self.assertRaises(RouteException):
            self.assertTrue(request.route('not.exists', [1]))

    def test_request_route_returns_url_without_passing_args_with_current_param(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', [
            Get('/test/url', 'TestController@show').name('test.url'),
            Get('/test/url/@id', 'TestController@show').name('test.id')
        ])
        request = app.make('Request').load_app(app)
        request.url_params = {'id': 1}

        assert request.route('test.id') == '/test/url/1'

    def test_request_redirection(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', [
            Get('/test/url', 'TestController@show').name('test.url'),
            Get('/test/url/@id', 'TestController@testing').name('test.id'),
            Get('/test/url/object', TestController.show).name('test.object')
        ])
        request = app.make('Request').load_app(app)

        self.assertEqual(request.redirect('/test/url/@id', {'id': 1}).redirect_url, '/test/url/1')
        request.redirect_url = None
        self.assertEqual(request.redirect(name='test.url').redirect_url, '/test/url')
        request.redirect_url = None
        self.assertEqual(request.redirect(name='test.id', params={'id': 1}).redirect_url, '/test/url/1')
        request.redirect_url = None
        self.assertEqual(request.redirect(controller='TestController@show').redirect_url, '/test/url')
        request.redirect_url = None
        self.assertEqual(request.redirect(controller=TestController.show).redirect_url, '/test/url/object')
        request.redirect_url = None
        self.assertEqual(request.redirect('some/url').redirect_url, '/some/url')

    def test_request_route_returns_full_url(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', [
            Get('/test/url', 'TestController@show').name('test.url'),
            Get('/test/url/@id', 'TestController@show').name('test.id')
        ])
        request = app.make('Request').load_app(app)

        self.assertEqual(request.route('test.url', full=True), 'http://localhost:8000/test/url')

    def test_redirect_compiles_url_with_multiple_slashes(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = 'test/url/here'

        self.assertEqual(request.compile_route_to_url(route), '/test/url/here')

    def test_redirect_compiles_url_with_trailing_slash(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = 'test/url/here/'

        self.assertEqual(request.compile_route_to_url(route), '/test/url/here/')

    def test_redirect_compiles_url_with_parameters(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = 'test/@id'
        params = {
            'id': '1',
        }

        self.assertEqual(request.compile_route_to_url(route, params), '/test/1')

    def test_redirect_compiles_url_with_list_parameters(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = 'test/@id'
        params = ['1']

        self.assertEqual(request.compile_route_to_url(route, params), '/test/1')

        route = 'test/@id/@user/test/@slug'
        params = ['1', '2', '3']

        self.assertEqual(request.compile_route_to_url(route, params), '/test/1/2/test/3')

    def test_redirect_compiles_url_with_multiple_parameters(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = 'test/@id/@test'
        params = {
            'id': '1',
            'test': 'user',
        }
        self.assertEqual(request.compile_route_to_url(route, params), '/test/1/user')

    def test_request_compiles_custom_route_compiler(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = 'test/@id:signed'
        params = {
            'id': '1',
        }
        self.assertEqual(request.compile_route_to_url(route, params), '/test/1')

    def test_redirect_compiles_url_with_http(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        route = "http://google.com"

        self.assertEqual(request.compile_route_to_url(route), 'http://google.com')

    def test_can_get_nully_value(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request._set_standardized_request_variables({
            "gateway": "RENDIMENTO",
            "request": {
                "user": "data"
            },
            "response": None,
            "description": "test only"
        })

    def test_can_get_nully_value_with_dictdot(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request._set_standardized_request_variables({
            "gateway": "RENDIMENTO",
            "request": {
                "user": "data",
                "age": None,
            },
            "response": None,
            "description": "test only"
        })

        self.assertEqual(request.input('request.age'), None)

    def test_can_get_list_as_root_payload(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request._set_standardized_request_variables([{"key": "val"}, {"item2": "val2"}])

        self.assertEqual(request.input(0)['key'], 'val')
        self.assertEqual(request.input('0')['key'], 'val')
        self.assertEqual(request.input(2), None)

    def test_can_get_list_as_root_payload_getting_all(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request._set_standardized_request_variables([{"key": "val"}, {"item2": "val2"}])

        self.assertIsInstance(request.all(), list)
        self.assertEqual(request.all()[0]['key'], 'val')

    def test_can_get_list_as_root_payload_as_dot_notation(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request._set_standardized_request_variables([{"key": "val"}, {"item2": "val2", "inner": {"value": "innervalue"}}, {"item3": [1,2]}])

        self.assertEqual(request.input('0.key'), 'val')
        self.assertEqual(request.input('1.item2'), 'val2')
        self.assertEqual(request.input('1.inner.value'), 'innervalue')
        self.assertEqual(request.input('2.item3.0'), 1)
        self.assertEqual(request.input('3.item3'), False)

    def test_request_gets_correct_header(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        self.assertEqual(request.header('HTTP_UPGRADE_INSECURE_REQUESTS'), '1')
        self.assertEqual(request.header('RAW_URI'), '/')
        self.assertEqual(request.header('NOT_IN'), '')
        self.assertFalse('text/html' in request.header('NOT_IN'))

    def test_request_sets_correct_header(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request.header('TEST', 'set_this')
        self.assertEqual(request.header('TEST'), 'set_this')

        request.header('TEST', 'set_this', http_prefix=True)
        self.assertEqual(request.header('HTTP_TEST'), 'set_this')

    def test_request_cant_set_multiple_headers(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request.header('TEST', 'test_this')
        request.header('TEST', 'test_that')

        self.assertEqual(request.header('TEST'), 'test_that')

    def test_request_sets_headers_with_dictionary(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request.header({
            'test_dict': 'test_value',
            'test_dict1': 'test_value1'
        })

        self.assertEqual(request.header('test_dict'), 'test_value')
        self.assertEqual(request.header('test_dict1'), 'test_value1')

        request.header({
            'test_dict': 'test_value',
            'test_dict1': 'test_value1'
        }, http_prefix=True)

        self.assertEqual(request.header('HTTP_test_dict'), 'test_value')
        self.assertEqual(request.header('HTTP_test_dict1'), 'test_value1')

    def test_request_gets_all_headers(self):
        app = App()
        app.bind('Request', Request(wsgi_request))
        request = app.make('Request').load_app(app)

        request.header('TEST1', 'set_this_item')
        self.assertEqual(request.get_headers(), [('TEST1', 'set_this_item')])

    def test_request_sets_str_status_code(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('StatusCode', 'TestController@show')
        request = app.make('Request').load_app(app)

        request.status('200 OK')
        self.assertEqual(request.get_status_code(), '200 OK')

    def test_request_sets_int_status_code(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request.status(500)
        self.assertEqual(request.get_status_code(), '500 Internal Server Error')

    def test_request_gets_int_status(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request.status(500)
        self.assertEqual(request.get_status(), 500)

    def test_can_get_code_by_value(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request.status(500)
        self.assertEqual(request._get_status_code_by_value('500 Internal Server Error'), 500)

    def test_is_status_code(self):
        app = App()
        app.bind('Request', self.request)
        request = app.make('Request').load_app(app)

        request.status(500)
        self.assertEqual(request.is_status(500), True)

    def test_request_sets_invalid_int_status_code(self):
        with self.assertRaises(InvalidHTTPStatusCode):
            app = App()
            app.bind('Request', self.request)
            request = app.make('Request').load_app(app)

            request.status(600)

    def test_request_sets_request_method(self):
        wsgi = generate_wsgi()
        wsgi['QUERY_STRING'] = '__method=PUT'
        request = Request(wsgi)

        assert request.has('__method')
        self.assertEqual(request.input('__method'), 'PUT')
        self.assertEqual(request.get_request_method(), 'PUT')

    def test_request_has_should_pop_variables_from_input(self):
        self.request.request_variables.update({'key1': 'test', 'key2': 'test'})
        self.request.pop('key1', 'key2')
        self.assertEqual(self.request.request_variables, {'application': 'Masonite'})
        self.request.pop('shouldnotexist')
        self.assertEqual(self.request.request_variables, {'application': 'Masonite'})
        self.request.pop('application')
        self.assertEqual(self.request.request_variables, {})

    def test_is_named_route(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', [
            Get('/test/url', 'TestController@show').name('test.url'),
            Get('/test/url/@id', 'TestController@show').name('test.id')
        ])
        request = app.make('Request').load_app(app)

        request.path = '/test/url'
        assert request.is_named_route('test.url')

        request.path = '/test/url/1'
        assert request.is_named_route('test.id', {'id': 1})

    def test_route_exists(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', [
            Get('/test/url', 'TestController@show').name('test.url'),
            Get('/test/url/@id', 'TestController@show').name('test.id')
        ])
        request = app.make('Request').load_app(app)

        self.assertEqual(request.route_exists('/test/url'), True)
        self.assertEqual(request.route_exists('/test/Not'), False)

    def test_request_url_from_controller(self):
        app = App()
        app.bind('Request', self.request)
        app.bind('WebRoutes', [
            Get('/test/url', 'TestController@show').name('test.url'),
            Get('/test/url/@id', 'ControllerTest@show').name('test.id'),
            Get('/test/url/controller/@id', TestController.show).name('test.controller'),
        ])

        request = app.make('Request').load_app(app)

        self.assertEqual(request.url_from_controller('TestController@show'), '/test/url')
        self.assertEqual(request.url_from_controller('ControllerTest@show', {'id': 1}), '/test/url/1')
        self.assertEqual(request.url_from_controller(TestController.show, {'id': 1}), '/test/url/controller/1')

    def test_contains_for_path_detection(self):
        self.request.path = '/test/path'
        self.assertTrue(self.request.contains('/test/*'))
        self.assertTrue(self.request.contains('/test/path'))
        self.assertFalse(self.request.contains('/test/wrong'))

    def test_contains_for_multiple_paths(self):
        self.request.path = '/test/path/5'
        self.assertTrue(self.request.contains('/test/*'))

    def test_contains_can_return_string(self):
        self.request.path = '/test/path/5'
        self.assertEqual(self.request.contains('/test/*', show='active'), 'active')
        self.assertEqual(self.request.contains('/test/not', show='active'), '')

    def test_contains_for_path_with_digit(self):
        self.request.path = '/test/path/1'
        self.assertTrue(self.request.contains('/test/path/*'))
        self.assertTrue(self.request.contains('/test/path/*:int'))

    def test_contains_for_path_with_digit_and_wrong_contains(self):
        self.request.path = '/test/path/joe'
        self.assertFalse(self.request.contains('/test/path/*:int'))

    def test_contains_for_path_with_alpha_contains(self):
        self.request.path = '/test/path/joe'
        self.assertTrue(self.request.contains('/test/path/*:string'))

    def test_contains_for_route_compilers(self):
        self.request.path = '/test/path/joe'
        self.assertTrue(self.request.contains('/test/path/*:signed'))

    def test_contains_multiple_asteriks(self):
        self.request.path = '/dashboard/user/edit/1'
        self.assertTrue(self.request.contains('/dashboard/user/*:string/*:int'))

    def test_request_can_get_input_as_properties(self):
        self.request.request_variables = {'test': 'hey'}
        self.assertEqual(self.request.test, 'hey')
        self.assertEqual(self.request.input('test'), 'hey')

    def test_request_can_get_param_as_properties(self):
        self.request.url_params = {'test': 'hey'}
        self.assertEqual(self.request.test, 'hey')
        self.assertEqual(self.request.param('test'), 'hey')

    def test_back_returns_correct_url(self):
        self.request.path = '/dashboard/create'
        self.request.back()
        self.assertEqual(self.request.redirect_url, '/dashboard/create')

        self.request.back(default='/home')
        self.assertEqual(self.request.redirect_url, '/home')

        self.request.request_variables = {'__back': '/login'}
        self.request.back(default='/home')
        self.assertEqual(self.request.redirect_url, '/login')

    def test_request_without(self):
        self.request.request_variables.update({'__token': 'testing', 'application': 'Masonite'})
        self.assertEqual(self.request.without('__token'), {'application': 'Masonite'})

    def test_request_only_returns_specified_values(self):
        self.request.request_variables.update({'__token': 'testing', 'application': 'Masonite'})
        self.assertEqual(self.request.only('application'), {'application': 'Masonite'})
        self.assertEqual(self.request.only('__token'), {'__token': 'testing'})

    def test_request_gets_only_clean_output(self):
        self.request._set_standardized_request_variables({'key': '<img """><script>alert(\'hey\')</script>">'})
        self.assertEqual(self.request.input('key', clean=True), '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;')
        self.assertEqual(self.request.input('key', clean=False), '<img """><script>alert(\'hey\')</script>">')

    def test_request_cleans_all_optionally(self):
        self.request._set_standardized_request_variables({'key': '<img """><script>alert(\'hey\')</script>">'})
        self.assertEqual(self.request.all()['key'], '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;')
        self.assertEqual(self.request.all(clean=False)['key'], '<img """><script>alert(\'hey\')</script>">')

    def test_request_gets_input_with_dotdict(self):
        self.request.request_variables = {
            "key": {
                "user": "1",
                        "name": "Joe",
                        "address": {
                            "street": "address 1"
                        }
            }
        }

        self.assertEqual(self.request.input('key')['address']['street'], 'address 1')
        self.assertEqual(self.request.input('key.address.street'), 'address 1')
        self.assertEqual(self.request.input('key.'), False)
        self.assertEqual(self.request.input('key.user'), '1')
        self.assertEqual(self.request.input('key.nothing'), False)
        self.assertEqual(self.request.input('key.nothing', default='test'), 'test')
