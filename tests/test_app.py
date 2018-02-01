from masonite.app import App
from masonite.request import Request
from masonite.routes import Get, Post
import inspect
import pytest

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

REQUEST = Request(wsgi_request).key(
    'NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY=')
print(REQUEST.__class__)

def functest(Request, get: Get, post: Post):
    print('route_url', get.route_url)
    return Request.cookies


def test_app_binds():
    app = App()

    app.bind('test1', object)
    app.bind('test2', object)

    assert app.providers == {'test1': object, 'test2': object}

def test_app_makes():
    app = App()
    app.bind('Request', REQUEST)
    assert app.make('Request').cookies == []

def test_throws_exception_if_too_many_bindings():
    app = App()
    REQUEST.cookies = ['hey']
    app.bind('Request', REQUEST)
    app.bind('Route', Get().route('test/', None))
    print(inspect.getfullargspec(functest))
    with pytest.raises(TypeError, message="should raise error"):
        app.resolve(functest)
