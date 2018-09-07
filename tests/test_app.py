from masonite.app import App
from masonite.request import Request
from masonite.routes import Get, Post
from masonite.exceptions import ContainerError
from masonite.testsuite.TestSuite import generate_wsgi
import inspect
import pytest

REQUEST = Request({}).load_environ(generate_wsgi())


class TestApp:

    def setup_method(self):
        self.app = App()

    def test_app_binds(self):
        self.app.bind('test1', object)
        self.app.bind('test2', object)
        assert self.app.providers == {'test1': object, 'test2': object}

    def test_app_simple_bind(self):
        self.app.simple(Request)
        assert self.app.providers == {'masonite.request.Request': Request}

    def test_app_simple_bind_init(self):
        req = Request()
        self.app.simple(req)
        assert self.app.providers == {'masonite.request.Request': req}

    def test_app_makes(self):
        self.app.bind('Request', REQUEST)
        assert self.app.make('Request').cookies == []

    def test_throws_exception_if_too_many_bindings(self):
        REQUEST.cookies = ['hey']
        self.app.bind('Request', REQUEST)
        self.app.bind('Route', Get().route('test/', None))
        with pytest.raises(ContainerError, message="should raise error"):
            self.app.resolve(self._functest)

    def _functest(Request, get: Get, post: Post):
        return Request.cookies

    def test_can_set_container_hook(self):
        self.app.on_bind('Request', self._func_on_bind)
        self.app.bind('Request', REQUEST)
        assert self.app.make('Request').path == '/test/on/bind'

    def _func_on_bind(self, request, container):
        request.path = '/test/on/bind'

    def test_can_set_container_hook_with_obj_binding(self):
        self.app.on_bind(Request, self._func_on_bind_with_obj)
        self.app.bind('Request', REQUEST)
        assert self.app.make('Request').path == '/test/on/bind/obj'

    def _func_on_bind_with_obj(self, request, container):
        request.path = '/test/on/bind/obj'

    def test_can_fire_container_hook_on_make(self):
        self.app.on_make(Request, self._func_on_make)
        self.app.bind('Request', REQUEST)
        assert self.app.make('Request').path == '/test/on/make'

    def _func_on_make(self, request, container):
        request.path = '/test/on/make'

    def test_can_fire_hook_on_resolve(self):
        self.app.on_resolve(Request, self._func_on_resolve)
        self.app.bind('Request', REQUEST)
        assert self.app.resolve(self._resolve_request).path == '/on/resolve'

    def test_can_fire_hook_on_resolve_class(self):
        self.app.on_resolve(Request, self._func_on_resolve_class)
        self.app.bind('Request', REQUEST)
        assert self.app.resolve(
            self._resolve_reques_class).path == '/on/resolve/class'

    def test_can_resolve_parameter_with_keyword_argument_setting(self):
        self.app.bind('Request', REQUEST)
        self.app.resolve_parameters = True
        assert self.app.resolve(
            self._resolve_parameter) == REQUEST

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
