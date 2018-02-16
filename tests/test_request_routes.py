from masonite.routes import Get, Post
from masonite.request import Request
from masonite.testsuite.TestSuite import TestSuite

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

def test_get_initialized():
    assert callable(Get)
    assert callable(Post)

def test_get_sets_route():
    assert Get().route('test', None)

def test_sets_name():
    get = Get().route('test', None).name('test')

    assert get.named_route == 'test'

def test_loads_request():
    get = Get().route('test', None).name('test').load_request('test')

    assert get.request == 'test'

def test_loads_middleware():
    get = Get().route('test', None).middleware('auth', 'middleware')

    assert get.list_middleware == ('auth', 'middleware')

def test_method_type():
    assert Post().method_type == 'POST'
    assert Get().method_type == 'GET'

def test_method_type_sets_domain():
    get = Get().domain('test')
    post = Post().domain('test')

    assert get.required_domain == 'test'
    assert post.required_domain == 'test'

def test_method_type_has_required_subdomain():
    get = Get().domain('test')
    post = Get().domain('test')

    REQUEST.environ['HTTP_HOST'] = 'test.localhost:8000'

    get.request = REQUEST
    post.request = REQUEST

    assert get.has_required_domain() == True
    assert post.has_required_domain() == True

def test_method_type_has_required_subdomain_with_asterick():
    container = TestSuite().create_container()
    request = container.container.make('Request')

    request.environ['HTTP_HOST'] = 'test.localhost:8000'

    get = Get().domain('*')
    post = Get().domain('*')

    get.request = request
    post.request = request

    assert get.has_required_domain() == True
    assert post.has_required_domain() == True


def test_request_sets_subdomain_on_get():
    
    container = TestSuite().create_container()
    request = container.container.make('Request')

    request.environ['HTTP_HOST'] = 'test.localhost:8000'

    get = Get().domain('*')
    post = Get().domain('*')

    get.request = request
    post.request = request

    get.has_required_domain()
    assert request.param('subdomain') == 'test'

def test_route_changes_module_location():

    get = Get().module('app.test')
    post = Get().module('app.test')

    assert get.module_location == 'app.test'
