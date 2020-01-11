from src.masonite.app import App
from src.masonite.request import Request
from src.masonite.testing import generate_wsgi
import unittest

REQUEST = Request({}).load_environ(generate_wsgi())


class MockMail:

    def __init__(self, request: Request):
        self.request = request


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_app_binds(self):
        self.app.bind('test1', object)
        self.app.bind('test2', object)
        self.assertEqual(self.app.providers, {'test1': object, 'test2': object})

    def test_app_makes(self):
        self.app.bind('Request', REQUEST)
        self.assertEqual(self.app.make('Request').cookies, [])

    def test_app_makes_and_resolves(self):
        self.app.bind('Request', REQUEST)
        self.app.bind('MockMail', MockMail)
        mockmail = self.app.make('MockMail')
        self.assertIsInstance(mockmail.request, Request)

    def test_app_makes_different_instances(self):
        self.app.bind('MockMail', MockMail)
        self.app.bind('Request', REQUEST)
        m1 = self.app.make('MockMail')
        m2 = self.app.make('MockMail')

        self.assertNotEqual(id(m1), id(m2))

    def test_app_makes_singleton_instance(self):
        self.app.bind('Request', REQUEST)
        self.app.singleton('MockMail', MockMail)
        m1 = self.app.make('MockMail')
        m2 = self.app.make('MockMail')

        self.assertEqual(id(m1), id(m2))
        self.assertEqual(id(m1.request), id(m2.request))

        m1.request.test = 'test'
        self.assertEqual(m2.request.test, 'test')

    def test_can_set_container_hook(self):
        self.app.on_bind('Request', self._func_on_bind)
        self.app.bind('Request', REQUEST)
        self.assertEqual(self.app.make('Request').path, '/test/on/bind')

    def _func_on_bind(self, request, container):
        request.path = '/test/on/bind'

    def test_can_set_container_hook_with_obj_binding(self):
        self.app.on_bind(Request, self._func_on_bind_with_obj)
        self.app.bind('Request', REQUEST)
        self.assertEqual(self.app.make('Request').path, '/test/on/bind/obj')

    def _func_on_bind_with_obj(self, request, container):
        request.path = '/test/on/bind/obj'

    def test_can_fire_container_hook_on_make(self):
        self.app.on_make(Request, self._func_on_make)
        self.app.bind('Request', REQUEST)
        self.assertEqual(self.app.make('Request').path, '/test/on/make')
        self.assertEqual(self.app.make('Request').path, '/test/on/make')

    def _func_on_make(self, request, container):
        request.path = '/test/on/make'

    def test_can_fire_hook_on_resolve(self):
        self.app.on_resolve(Request, self._func_on_resolve)
        self.app.bind('Request', REQUEST)
        self.assertEqual(self.app.resolve(self._resolve_request).path, '/on/resolve')
        self.assertEqual(self.app.resolve(self._resolve_request).path, '/on/resolve')

    def test_can_fire_hook_on_resolve_class(self):
        self.app.on_resolve(Request, self._func_on_resolve_class)
        self.app.bind('Request', REQUEST)
        self.assertEqual(self.app.resolve(self._resolve_reques_class).path, '/on/resolve/class')
        self.assertEqual(self.app.resolve(self._resolve_reques_class).path, '/on/resolve/class')

    def test_can_resolve_parameter_with_keyword_argument_setting(self):
        self.app.bind('Request', REQUEST)
        self.app.resolve_parameters = True
        self.assertEqual(self.app.resolve(self._resolve_parameter), REQUEST)
        self.assertEqual(self.app.resolve(self._resolve_parameter), REQUEST)

    def _func_on_resolve(self, request, container):
        request.path = '/on/resolve'

    def _func_on_resolve_class(self, request, container):
        request.path = '/on/resolve/class'

    def _resolve_request(self, request: Request):
        return request

    def _resolve_parameter(self, Request):
        return Request

    def _resolve_reques_class(self, request: Request):
        return request
