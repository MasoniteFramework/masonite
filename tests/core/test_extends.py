from src.masonite.app import App
from src.masonite.testing import generate_wsgi, MockWsgiInput
from src.masonite.routes import Route
from src.masonite.request import Request

wsgi_request = generate_wsgi()
import unittest


class ExtendClass:

    path = None

    def get_path(self):
        return self.path

    def get_another_path(self):
        return self.path


class ExtendClass2:

    path = None

    def get_path2(self):
        return self.path

    def get_another_path2(self):
        return self.path


def get_third_path(self):
    return self.path


class TestExtends(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.request = Request(wsgi_request)
        self.app.bind('Request', self.request)

    def test_request_can_extend(self):
        request = self.app.make('Request').load_app(self.app)

        request.extend('get_path', ExtendClass.get_path)
        request.extend('get_another_path_test', ExtendClass.get_another_path)
        request.extend('get_third_path_test', get_third_path)

        self.assertEqual(request.get_path(), '/')
        self.assertEqual(request.get_another_path_test(), '/')
        self.assertEqual(request.get_third_path_test(), '/')

        request.extend(ExtendClass2)

        self.assertEqual(request.get_path2(), '/')
        self.assertEqual(request.get_another_path2(), '/')

        request.extend(get_third_path)
        self.assertEqual(request.get_third_path(), '/')

        request.extend(ExtendClass.get_another_path)
        self.assertEqual(request.get_another_path(), '/')

    def test_gets_input_and_query_with_get_request(self):
        app = App()
        wsgi_environ = generate_wsgi()
        wsgi_environ['QUERY_STRING'] = 'param=1&param=2&param=3&foo=bar&q=yes'
        wsgi_environ['wsgi.input'] = {'param': 'hey', 'foo': [9, 8, 7, 6], 'bar': 'baz'}
        wsgi_environ['REQUEST_METHOD'] = 'GET'

        route_class = Route(wsgi_environ)
        request_class = Request(wsgi_environ)
        app.bind('Request', request_class)
        app.bind('Route', route_class)
        request = app.make('Request').load_app(app)

        self.assertEqual(request.query('param'), '1')
        self.assertEqual(request.all_query()['param'], ['1', '2', '3'])
        self.assertEqual(request.query('foo'), 'bar')
        self.assertEqual(request.query('param', multi=True), ['1', '2', '3'])
        self.assertEqual(request.query('not-exist', default=2), 2)
        self.assertEqual(request.query('not-exist', default=2, multi=True), 2)
        self.assertEqual(request.query('q', default='no'), 'yes')

        self.assertEqual(request.input('foo'), 'bar')
        self.assertEqual(request.input('param'), '1')
        self.assertEqual(request.input('q', default='no'), 'yes')
        self.assertEqual(request.input('bar', default='default'), 'default')

    def test_gets_input_and_query_with_non_get_request(self):
        app = App()

        for method in ['POST', 'PUT', 'DELETE']:
            wsgi_environ = generate_wsgi()
            wsgi_environ['REQUEST_METHOD'] = method
            wsgi_environ['QUERY_STRING'] = 'param=1&param=2&param=3&foo=bar&q=yes'
            wsgi_environ['wsgi.input'] = MockWsgiInput('{"param": "hey", "foo": [9, 8, 7, 6], "bar": "baz"}')
            wsgi_environ['CONTENT_TYPE'] = 'application/json'
            route_class = Route(wsgi_environ)
            request_class = Request(wsgi_environ)
            app.bind('Request', request_class)
            app.bind('Route', route_class)
            request = app.make('Request').load_app(app)

            self.assertEqual(request.input('foo'), [9, 8, 7, 6])
            self.assertEqual(request.input('param'), 'hey')
            self.assertEqual(request.input('not-exist', default=2), 2)
            self.assertEqual(request.input('q', default='default'), 'default')
            self.assertEqual(request.input('bar', default='default'), 'baz')
            self.assertEqual(request.query('foo'), 'bar')
            self.assertEqual(request.query('param'), '1')
            self.assertEqual(request.query('param', multi=True), ['1', '2', '3'])
            self.assertEqual(request.query('not-exist', default=2), 2)
            self.assertEqual(request.query('not-exist', default=2, multi=True), 2)
            self.assertEqual(request.query('q', default='default'), 'yes')

    def test_hidden_form_request_method_changes_request_method(self):
        app = App()
        wsgi_request = generate_wsgi()
        wsgi_request['POST_DATA'] = '__method=PUT'
        request_class = Request(wsgi_request)
        self.assertEqual(request_class.environ['REQUEST_METHOD'], 'PUT')

    def test_get_json_input(self):
        json_wsgi = wsgi_request
        json_wsgi['REQUEST_METHOD'] = 'POST'
        json_wsgi['CONTENT_TYPE'] = 'application/json'
        json_wsgi['POST_DATA'] = ''
        json_wsgi['wsgi.input'] = MockWsgiInput('{"id": 1, "test": "testing"}')
        Route(json_wsgi)
        request_obj = Request(json_wsgi)

        self.assertIsInstance(request_obj.request_variables, dict)
        self.assertEqual(request_obj.input('id'), 1)
        self.assertEqual(request_obj.input('test'), 'testing')
