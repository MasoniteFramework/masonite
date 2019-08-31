from config import application, providers

from masonite.app import App
from masonite.routes import Get
from masonite.testsuite.TestSuite import TestSuite, generate_wsgi
import unittest
from masonite.helpers import config


class TestProviders(unittest.TestCase):

    def setUp(self):
        self.app = App(remember=False)
        self.app.bind('WSGI', object)

        # self.app.bind('Providers', providers)
        self.app.bind('Environ', generate_wsgi())

    def test_providers_load_into_container(self):
        for provider in config('providers.providers'):
            provider().load_app(self.app).register()

        self.app.bind('Response', 'test')
        self.app.bind('WebRoutes', [
            Get().route('url', 'TestController@show'),
            Get().route('url/', 'TestController@show'),
            Get().route('url/@firstname', 'TestController@show'),
        ])

        self.app.bind('Response', 'Route not found. Error 404')

        for provider in config('providers.providers'):
            self.app.resolve(provider().load_app(self.app).boot)

        self.assertTrue(self.app.make('Request'))

    def test_normal_app_containers(self):
        self.app = TestSuite().create_container()
        self.assertTrue(self.app.get_container().make('Request'))
