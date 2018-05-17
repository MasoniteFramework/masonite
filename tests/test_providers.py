from pydoc import locate
from config import application

from masonite.app import App
from masonite.routes import Get
from masonite.testsuite.TestSuite import TestSuite, generate_wsgi


container = App()
container.bind('WSGI', object)

container.bind('Application', application)
container.bind('Environ', generate_wsgi())


def test_providers_load_into_container():

    for provider in container.make('Application').PROVIDERS:
        container.resolve(locate(provider)().load_app(container).register)

    container.bind('Response', 'test')
    container.bind('WebRoutes', [
        Get().route('url', None),
        Get().route('url/', None),
        Get().route('url/@firstname', None),
    ])

    container.bind('Response', 'Route not found. Error 404')

    for provider in container.make('Application').PROVIDERS:
        located_provider = locate(provider)().load_app(container)

        container.resolve(locate(provider)().load_app(container).boot)

    assert container.make('Request')


def test_normal_app_containers():
    container = TestSuite().create_container()
    assert container.get_container().make('Request')
