from masonite.app import App
from pydoc import locate
from config import application
from masonite.routes import Get, Api
from masonite.testsuite.TestSuite import TestSuite

container = App()
container.bind('WSGI', object)
wsgi_request = {
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

container.bind('Application', application)
container.bind('Environ', wsgi_request)

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
    container.bind('ApiRoutes', [
        Api().model(object),
        Api().model(object),
    ])

    for provider in container.make('Application').PROVIDERS:
        located_provider = locate(provider)().load_app(container)

        container.resolve(locate(provider)().load_app(container).boot)

    assert container.make('Request')

def test_normal_app_containers():
    container = TestSuite().create_container()
    assert container.get_container().make('Request')
