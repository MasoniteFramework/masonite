from pydoc import locate
from config import application, providers

from masonite.app import App
from masonite.routes import Get
from masonite.testsuite.TestSuite import TestSuite, generate_wsgi


class TestProviders:

    def setup_method(self):
        self.app = App()
        self.app.bind('WSGI', object)

        self.app.bind('Application', application)
        self.app.bind('Providers', providers)
        self.app.bind('Environ', generate_wsgi())

    def test_providers_load_into_container(self):
        for provider in self.app.make('Providers').PROVIDERS:
            self.app.resolve(provider().load_app(self.app).register)

        self.app.bind('Response', 'test')
        self.app.bind('WebRoutes', [
            Get().route('url', None),
            Get().route('url/', None),
            Get().route('url/@firstname', None),
        ])

        self.app.bind('Response', 'Route not found. Error 404')

        for provider in self.app.make('Providers').PROVIDERS:
            provider().load_app(self.app)

            self.app.resolve(provider().load_app(self.app).boot)

        assert self.app.make('Request')

    def test_normal_app_containers(self):
        self.app = TestSuite().create_container()
        assert self.app.get_container().make('Request')
