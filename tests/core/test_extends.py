from masonite.app import App
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.routes import Route
from masonite.request import Request

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


class MockWsgiInput():

    def read(self, value):
        return '{"id": 1, "test": "testing"}'


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

    def test_gets_input_with_all_request_methods(self):
        app = App()
        wsgi_request['QUERY_STRING'] = 'hey=test'
        request_class = Request(wsgi_request)
        app.bind('Request', request_class)
        request = app.make('Request').load_app(app)

        request.environ['REQUEST_METHOD'] = 'GET'
        self.assertEqual(request.input('hey'), 'test')

        request.environ['REQUEST_METHOD'] = 'POST'
        self.assertEqual(request.input('hey'), 'test')

        request.environ['REQUEST_METHOD'] = 'PUT'
        self.assertEqual(request.input('hey'), 'test')

        request.environ['REQUEST_METHOD'] = 'PATCH'
        self.assertEqual(request.input('hey'), 'test')

        request.environ['REQUEST_METHOD'] = 'DELETE'
        self.assertEqual(request.input('hey'), 'test')

    def test_hidden_form_request_method_changes_request_method(self):
        app = App()
        wsgi_request['QUERY_STRING'] = '__method=PUT'
        request_class = Request(wsgi_request)

        app.bind('Request', request_class)
        request = app.make('Request').load_app(app)

        self.assertEqual(request.environ['REQUEST_METHOD'], 'PUT')

    def test_get_json_input(self):
        json_wsgi = wsgi_request
        json_wsgi['REQUEST_METHOD'] = 'POST'
        json_wsgi['CONTENT_TYPE'] = 'application/json'
        json_wsgi['QUERY_STRING'] = ''
        json_wsgi['wsgi.input'] = MockWsgiInput()
        Route(json_wsgi)
        request_obj = Request(json_wsgi)

        self.assertIsInstance(request_obj.request_variables, dict)
        self.assertEqual(request_obj.input('id'), 1)
        self.assertEqual(request_obj.input('test'), 'testing')
