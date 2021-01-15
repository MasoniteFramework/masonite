from src.masonite.app import App
from src.masonite.exception_handler import ExceptionHandler
from src.masonite.hook import Hook
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.testing import generate_wsgi
from src.masonite.view import View
import unittest


class ApplicationMock:
    DEBUG = True


class StorageMock:
    STATICFILES = {}


class MockExceptionHandler:

    def __init__(self, request: Request):
        self.request = request

    def handle(self, _):
        self.request.header('test', 'test')


class TestException(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Environ', generate_wsgi())
        self.app.bind('WebRoutes', [])
        self.app.bind('View', View(self.app).render)
        self.app.bind('Request', Request(generate_wsgi()).load_app(self.app))
        self.app.bind('Response', Response(self.app))
        self.app.bind('StatusCode', None)
        self.app.bind('Storage', StorageMock)
        self.app.bind('ExceptionHandler', ExceptionHandler(self.app))
        self.app.bind('HookHandler', Hook(self.app))
        self.app.bind('Request', Request(generate_wsgi()).load_app(self.app))
        self.app.bind('staticfiles', {})
        self.app.bind('ExceptionAttributeErrorHandler', MockExceptionHandler)

    def test_exception_renders_view(self):
        self.app.make('ExceptionHandler').load_exception(OSError)
        self.assertIsNotNone(self.app.make('Response'))

    def test_exception_uses_custom_exception(self):
        try:
            self.app.false()
        except Exception as e:
            self.app.make('ExceptionHandler').load_exception(e)

        self.assertEqual(self.app.make('Request').header('test'), 'test')

    def test_custom_exception_when_not_registered(self):
        try:
            self.app.false()
        except Exception as e:
            self.app.make('ExceptionHandler').load_exception(e)

    def test_exception_returns_none_when_debug_is_false(self):
        # config('application.debug') = False
        self.assertIsNone(self.app.make('ExceptionHandler').load_exception(KeyError))
