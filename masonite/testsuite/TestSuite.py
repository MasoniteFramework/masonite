from masonite.app import App
from masonite.testsuite.TestRoute import TestRoute
from masonite.testsuite.TestRequest import TestRequest

import io


def generate_wsgi():
    return {
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'wsgi.input': io.BytesIO(),
        'SERVER_SOFTWARE': 'gunicorn/19.7.1',
        'REQUEST_METHOD': 'GET',
        'QUERY_STRING': 'application=Masonite',
        'RAW_URI': '/',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'HTTP_HOST': '127.0.0.1:8000',
        'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'HTTP_UPGRADE_INSECURE_REQUESTS': '1',
        'HTTP_COOKIE': 'setcookie=value',
        'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
        'HTTP_ACCEPT_LANGUAGE': 'en-us',
        'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
        'HTTP_CONNECTION': 'keep-alive',
        'wsgi.url_scheme': 'http',
        'REMOTE_ADDR': '127.0.0.1',
        'REMOTE_PORT': '62241',
        'SERVER_NAME': '127.0.0.1',
        'SERVER_PORT': '8000',
        'PATH_INFO': '/',
        'SCRIPT_NAME': ''
    }


class TestSuite:

    def create_container(self, wsgi=generate_wsgi(), container=None, routes=[]):
        from config import application, providers
        if not container:
            container = App(remember=False)

        container.bind('WSGI', wsgi)
        container.bind('Application', application)
        container.bind('Container', container)
        container.bind('ProvidersConfig', providers)
        container.bind('Providers', [])
        container.bind('WSGIProviders', [])

        """
        |--------------------------------------------------------------------------
        | Bind all service providers
        |--------------------------------------------------------------------------
        |
        | Let's register everything into the Service Container. Once everything is
        | in the container we can run through all the boot methods. For reasons
        | some providers don't need to execute with every request and should
        | only run once when the server is started. Providers will be ran
        | once if the wsgi attribute on a provider is False.
        |
        """

        for provider in container.make('ProvidersConfig').PROVIDERS:
            located_provider = provider()
            located_provider.load_app(container).register()
            if located_provider.wsgi:
                container.make('WSGIProviders').append(located_provider)
            else:
                container.make('Providers').append(located_provider)

        for provider in container.make('Providers'):
            container.resolve(provider.boot)

        """
        |--------------------------------------------------------------------------
        | Startup the Service Container
        |--------------------------------------------------------------------------
        |
        | Instantiate the Service Container so we can bind classes into it and
        | bind the environ variable that is created by the WSGI server into
        | the container.
        |
        """

        container.bind('Environ', wsgi)

        """
        |--------------------------------------------------------------------------
        | Execute All Service Providers
        |--------------------------------------------------------------------------
        |
        | Run all service provider boot methods if the wsgi attribute is true.
        |
        """

        if routes:
            container.bind('WebRoutes', routes)

        for provider in container.make('WSGIProviders'):
            container.resolve(provider.boot)

        self.container = container
        return self

    def get_container(self):
        return self.container

    def route(self, route):
        return TestRoute(route)

    def get(self, route_url):
        return TestRequest().get(route_url)
