from masonite.routes import Route
from masonite.request import Request
from masonite.routes import Get, Post, Put, Patch, Delete


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


ROUTE = Route(wsgi_request)
REQUEST = Request(wsgi_request)


def test_route_is_callable():
    assert callable(Get)
    assert callable(Post)
    assert callable(Put)
    assert callable(Patch)
    assert callable(Delete)
        

def test_route_get_returns_output():
    assert ROUTE.get('url', 'output') == 'output'


def test_route_is_not_post():
    assert ROUTE.is_post() == False


def test_route_is_post():
    ROUTE.environ['REQUEST_METHOD'] = 'POST'
    assert ROUTE.is_post() == True


def test_compile_route_to_regex():
    assert ROUTE.compile_route_to_regex(Get().route('test/route', None)) == '^test\\/route\\/$'
    assert ROUTE.compile_route_to_regex(Get().route(
        'test/@route', None)) == '^test\\/(\\w+)\\/$'

    assert ROUTE.compile_route_to_regex(Get().route(
        'test/@route:int', None)) == '^test\\/(\\d+)\\/$'

    assert ROUTE.compile_route_to_regex(Get().route(
        'test/@route:string', None)) == '^test\\/([a-zA-Z]+)\\/$'


def test_route_url_list():
    assert ROUTE.generated_url_list() == ['route']


def test_route_gets_controllers():
    assert Get().route('test/url', 'TestController@show')
    assert Get().route('test/url', '/app.http.controllers.TestController@show')