import pytest

from masonite.app import App
from masonite.exception_handler import ExceptionHandler
from masonite.exceptions import MissingContainerBindingNotFound
from masonite.hook import Hook
from masonite.request import Request
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.view import View


class ApplicationMock:
    DEBUG = True

class StorageMock:
    STATICFILES = {}

class MockExceptionHandler:

    def __init__(self, request: Request):
        self.request = request

    def handle(self, exception):
        self.request.header('test', 'test', http_prefix=False)

class TestException:

    def setup_method(self):
        self.app = App()
        self.app.bind('Application', ApplicationMock)
        self.app.bind('Environ', generate_wsgi())
        self.app.bind('Response', None)
        self.app.bind('WebRoutes', [])
        self.app.bind('View', View(self.app).render)
        self.app.bind('Storage', StorageMock)
        self.app.bind('ExceptionHandler', ExceptionHandler(self.app))
        self.app.bind('HookHandler', Hook(self.app))
        self.app.bind('Request', Request(generate_wsgi()).load_app(self.app))
        self.app.bind('ExceptionAttributeErrorHandler', MockExceptionHandler)

    def test_exception_renders_view(self):
        self.app.make('ExceptionHandler').load_exception(OSError)
        assert self.app.make('Response') is not None

    def test_exception_uses_custom_exception(self):
        try:
            self.app.false()
        except Exception as e:
            self.app.make('ExceptionHandler').load_exception(e)
        
        assert self.app.make('Request').header('test') == 'test'

    def test_custom_exception_when_not_registered(self):
        try:
            self.app.false()
        except Exception as e:
            self.app.make('ExceptionHandler').load_exception(e)

    def test_exception_returns_none_when_debug_is_false(self):
        self.app.make('Application').DEBUG = False
        assert self.app.make('ExceptionHandler').load_exception(KeyError) is None
