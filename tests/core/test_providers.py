
import unittest

from src.masonite.app import App
from src.masonite.helpers import config
from src.masonite.routes import Get
from src.masonite.testing import TestCase, generate_wsgi


class TestProviders(TestCase):

    def setUp(self):
        super().setUp()
        self.container.bind('Environ', generate_wsgi())

    def test_providers_load_into_container(self):
        for provider in config('providers.providers'):
            provider().load_app(self.container).register()

        self.container.bind('Response', 'test')
        self.container.bind('WebRoutes', [
            Get().route('url', 'TestController@show'),
            Get().route('url/', 'TestController@show'),
            Get().route('url/@firstname', 'TestController@show'),
        ])

        self.container.bind('Response', 'Route not found. Error 404')

        for provider in config('providers.providers'):
            self.container.resolve(provider().load_app(self.container).boot)

        self.assertTrue(self.container.make('Request'))

    def test_normal_app_containers(self):
        self.assertTrue(self.container.make('Request'))
