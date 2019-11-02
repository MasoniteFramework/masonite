from src.masonite.providers import StatusCodeProvider
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.view import View
from src.masonite.app import App
from src.masonite.providers.StatusCodeProvider import ServerErrorExceptionHook
from src.masonite.testing import generate_wsgi
import unittest


class TestStatusCode(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('StatusCode', '404 Not Found')
        self.app.bind('Request', Request(None).load_app(self.app).load_environ(generate_wsgi()))
        self.app.simple(Response(self.app))
        self.app.bind('ViewClass', View(self.app))
        self.app.bind('View', self.app.make('ViewClass').render)

    def test_provider_returns_none_on_200_OK(self):
        self.assertIsNone(StatusCodeProvider().load_app(self.app).boot())


class MockApplicationConfig:
    DEBUG = 'True'


class TestServerErrorExceptionHook(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Container', self.app)
        self.app.bind('Request', Request(None).load_app(self.app).load_environ(generate_wsgi()))
        self.app.simple(Response)
        self.app.bind('Application', MockApplicationConfig)
        self.app.bind('ViewClass', View(self.app))
        self.app.bind('View', self.app.make('ViewClass').render)

    def test_response_is_set_when_app_debug_is_true(self):
        self.assertIsNone(ServerErrorExceptionHook().load(self.app))

    def test_no_response_set_when_app_debug_is_false(self):
        application = MockApplicationConfig
        application.DEBUG = False
        self.app.bind('Application', application)
        self.assertIsNone(ServerErrorExceptionHook().load(self.app))
