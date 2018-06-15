from masonite.app import App
from masonite.testsuite.TestRoute import TestRoute
from masonite.testsuite.TestRequest import TestRequest
from config import application, providers
from pydoc import locate


def generate_wsgi():
    return {
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
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

    def create_container(self):
        container = App()

        container.bind('WSGI', object)
        container.bind('Application', application)
        container.bind('Providers', providers)

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

        for provider in container.make('Providers').PROVIDERS:
            provider().load_app(container).register()

        for provider in container.make('Providers').PROVIDERS:
            located_provider = provider().load_app(container)

            if located_provider.wsgi is False:
                container.resolve(located_provider.boot)

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

        container.bind('Environ', generate_wsgi())

        """
        |--------------------------------------------------------------------------
        | Execute All Service Providers
        |--------------------------------------------------------------------------
        |
        | Run all service provider boot methods if the wsgi attribute is true.
        |
        """

        for provider in container.make('Providers').PROVIDERS:
            located_provider = provider().load_app(container)
            container.bind('Response', 'test')
            if located_provider.wsgi is True:
                container.resolve(located_provider.boot)

        self.container = container
        return self

    def get_container(self):
        return self.container

    def route(self, route):
        return TestRoute(route)

    def get(self, route_url):
        return TestRequest().get(route_url)
