from masonite.request import Request
from masonite.auth.Sign import Sign
from cryptography.fernet import Fernet

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
    'HTTP_COOKIE': '',
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

SECRET_KEY = 'pK1tLuZA8-upZGz-NiSCP_UVt-fxpxd796TaG6-dp8Y='
REQUEST = Request(wsgi_request).key(SECRET_KEY)


def test_set_and_get_cookie():
    REQUEST.cookie('test', 'testvalue')
    assert REQUEST.get_cookie('test') == 'testvalue'


def test_set_and_get_multiple_cookies():
    REQUEST.cookie('cookie1', 'cookie1value')
    REQUEST.cookie('cookie2', 'cookie2value')

    assert REQUEST.get_cookie('cookie1') == 'cookie1value'
    assert REQUEST.get_cookie('cookie2') == 'cookie2value'


def test_set_cookie_without_encryption():
    REQUEST.cookie('notencrypted', 'value', False)

    assert REQUEST.get_cookie('notencrypted', False) == 'value'


def test_set_and_get_cookie_with_no_existing_cookies():
    REQUEST.environ['HTTP_COOKIE'] = ''
    REQUEST.cookie('test', 'testvalue')
    assert REQUEST.get_cookie('test') == 'testvalue'


def test_set_and_get_cookie_with_existing_cookie():
    REQUEST.environ['HTTP_COOKIE'] = 'cookie=true'
    REQUEST.cookie('test', 'testvalue')
    assert REQUEST.get_cookie('test') == 'testvalue'


def test_set_and_get_cookie_with_http_only():
    REQUEST.cookie('test', 'testvalue')
    assert REQUEST.get_cookie('test') == 'testvalue'
    assert 'HttpOnly' in REQUEST.cookies[0][1]


def test_set_and_get_cookie_without_http_only():
    REQUEST.cookies = []
    REQUEST.cookie('test', 'testvalue', http_only=False, encrypt=False)
    assert REQUEST.get_cookie('test', decrypt=False) == 'testvalue'
    assert 'test=testvalue; Path=/' in REQUEST.cookies[0][1]
