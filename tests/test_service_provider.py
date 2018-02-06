from masonite.provider import ServiceProvider
from masonite.app import App
from masonite.request import Request
from masonite.routes import Get
import inspect

class ContainerTest(ServiceProvider):

    def boot(self, Request, Get):
        return Request

    def testboot(self, request: Request, Get: Get):
        return request

def test_service_provider_loads_app():
    app = App()
    provider = ServiceProvider()
    provider.load_app(app).boot()

    assert provider.app == app

def test_service_provider_sets_on_app_object():
    app = App()
    provider = ServiceProvider()
    provider.load_app(app).register()

    assert 'Request' in app.providers 
    assert app.make('Request') == object

def test_can_call_container_with_self_parameter():
    app = App()

    app.bind('Request', object)
    app.bind('Get', object)

    assert app.resolve(ContainerTest().boot) == app.make('Request')

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

def test_can_call_container_with_annotations_from_variable():
    app = App()

    request = Request(wsgi_request)

    app.bind('Request', request)
    app.bind('Get', Get().route('url', None))

    assert app.resolve(ContainerTest().testboot) == app.make('Request')


def test_can_call_container_with_annotation_with_self_parameter():
    app = App()

    app.bind('Request', Request)
    app.bind('Get', Get().route('url', None))

    assert app.resolve(ContainerTest().testboot) == app.make('Request')
