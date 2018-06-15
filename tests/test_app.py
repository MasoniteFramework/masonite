from masonite.app import App
from masonite.request import Request
from masonite.routes import Get, Post
from masonite.exceptions import ContainerError
import inspect
import pytest

REQUEST = Request({})

class TestApp:

    def setup_method(self):
        self.app = App()

    def test_app_binds(self):
        self.app.bind('test1', object)
        self.app.bind('test2', object)
        assert self.app.providers == {'test1': object, 'test2': object}

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