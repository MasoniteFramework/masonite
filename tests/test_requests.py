from config import application
from pydoc import locate

from masonite.request import Request
from masonite.app import App
from masonite.routes import Get, Route
from masonite.helpers.time import cookie_expire_time


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


def test_request_is_callable():
    """ Request should be callable """
    if callable(REQUEST):
        assert True


def test_request_input_should_return_input_on_get_request():
    assert REQUEST.input('application') == 'Masonite'

def test_request_all_should_return_params():
    assert REQUEST.all() == {'application': ['Masonite']}


def test_request_has_should_return_bool():
    assert REQUEST.has('application') == True
    assert REQUEST.has('shouldreturnfalse') == False


def test_request_set_params_should_return_self():
    assert REQUEST.set_params({'value': 'new'}) == REQUEST
    assert REQUEST.url_params == {'value': 'new'}


def test_request_param_returns_parameter_set_or_false():
    assert REQUEST.param('value') == 'new'
    assert REQUEST.param('nullvalue') == False


def test_request_appends_cookie():
    assert REQUEST.cookie('appendcookie', 'value') == REQUEST
    assert 'appendcookie' in REQUEST.environ['HTTP_COOKIE']


def test_request_sets_and_gets_cookies():
    REQUEST.cookie('setcookie', 'value') 
    assert REQUEST.get_cookie('setcookie') == 'value'


def test_request_sets_expiration_cookie_2_months():
    REQUEST.cookies = []
    REQUEST.cookie('setcookie_expiration', 'value', expires='2 months')

    time = cookie_expire_time('2 months')

    assert REQUEST.get_cookie('setcookie_expiration') == 'value'
    assert 'Expires={0}'.format(time) in REQUEST.cookies[0][1]


def test_delete_cookie():
    REQUEST.cookies = []
    REQUEST.cookie('delete_cookie', 'value')

    assert REQUEST.get_cookie('delete_cookie') == 'value'
    REQUEST.delete_cookie('delete_cookie')
    assert not REQUEST.get_cookie('delete_cookie')


def test_delete_cookie_with_wrong_key():
    REQUEST.cookies = []
    REQUEST.cookie('cookie', 'value')
    REQUEST.key('wrongkey_TXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY=')
    assert REQUEST.get_cookie('cookie') is None


def test_redirect_returns_request():
    assert REQUEST.redirect('newurl') == REQUEST
    assert REQUEST.redirect_url == 'newurl'


def test_redirectTo_returns_request():
    assert REQUEST.redirectTo('newroute') == REQUEST
    assert REQUEST.redirect_route == 'newroute'


def test_request_no_input_returns_false():
    assert REQUEST.input('notavailable') == False


def test_request_get_cookies_returns_cookies():
    assert REQUEST.get_cookies() == REQUEST.cookies


def test_request_set_user_sets_object():
    assert REQUEST.set_user(object) == REQUEST
    assert REQUEST.user_model == object
    assert REQUEST.user() == object


def test_request_loads_app():
    app = App()
    app.bind('Request', REQUEST)
    app.make('Request').load_app(app)

    assert REQUEST.app() == app
    assert app.make('Request').app() == app


def test_request_gets_input_from_container():
    container = App()
    container.bind('Application', application)
    container.bind('WSGI', object)
    container.bind('Environ', wsgi_request)

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

    assert container.make('Request').input('application') == 'Masonite'
    assert container.make('Request').all() == {'application': ['Masonite']}
    container.make('Request').environ['REQUEST_METHOD'] = 'POST'
    assert container.make('Request').environ['REQUEST_METHOD'] == 'POST'
    assert container.make('Request').input('application') == 'Masonite'


def test_redirections_reset():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('test')
    request.redirectTo('test')

    assert request.redirect_url is 'test'
    assert request.redirect_route is 'test'

    request.reset_redirections()

    assert request.redirect_url is False
    assert request.redirect_route is False


def test_request_has_subdomain_returns_bool():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    assert request.has_subdomain() is False
    assert request.subdomain is None

    request.environ['HTTP_HOST'] = 'test.localhost.com'

    assert request.has_subdomain() is True


def test_redirect_compiles_url():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('test/url')

    assert request.compile_route_to_url() == '/test/url'

def test_redirect_compiles_url_with_1_slash():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('/')

    assert request.compile_route_to_url() == '/'


def test_redirect_compiles_url_with_multiple_slashes():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('test/url/here')

    assert request.compile_route_to_url() == '/test/url/here'


def test_redirect_compiles_url_with_trailing_slash():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('test/url/here/')

    assert request.compile_route_to_url() == '/test/url/here/'


def test_redirect_compiles_url_with_parameters():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('test/@id').send({'id': '1'})

    assert request.compile_route_to_url() == '/test/1'


def test_redirect_compiles_url_with_multiple_parameters():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('test/@id/@test').send({'id': '1', 'test': 'user'})

    assert request.compile_route_to_url() == '/test/1/user'


def test_redirect_compiles_url_with_http():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.redirect('http://google.com')

    assert request.compile_route_to_url() == 'http://google.com'


def test_request_gets_correct_header():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    assert request.header('UPGRADE_INSECURE_REQUESTS') == '1'
    assert request.header('RAW_URI') == '/'
    assert request.header('NOT_IN') == None

def test_request_sets_correct_header():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.header('TEST', 'set_this')
    assert request.header('HTTP_TEST') == 'set_this'
    
    request.header('TEST', 'set_this', http_prefix = None)
    assert request.header('TEST') == 'set_this'


def test_request_gets_all_headers():
    app = App()
    app.bind('Request', Request(wsgi_request))
    request = app.make('Request').load_app(app)

    request.header('TEST1', 'set_this_item')
    request.header('TEST2', 'set_this_item', http_prefix = None)
    assert request.get_headers() == [('HTTP_TEST1', 'set_this_item'), ('TEST2', 'set_this_item')]


def test_request_sets_status_code():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.status('200 OK')
    assert request.get_status_code() == '200 OK'


class ExtendClass:

    path = None

    def get_path(self):
        return self.path

    def get_another_path(self):
        return self.path

class ExtendClass2:

    path = None

    def get_path2(self):
        return self.path

    def get_another_path2(self):
        return self.path

def get_third_path(self):
    return self.path

def test_request_can_extend():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)

    request.extend('get_path', ExtendClass.get_path)
    request.extend('get_another_path_test', ExtendClass.get_another_path)
    request.extend('get_third_path_test', get_third_path)

    assert request.get_path() == '/'
    assert request.get_another_path_test() == '/'
    assert request.get_third_path_test() == '/'

    request.extend(ExtendClass2)

    assert request.get_path2() == '/'
    assert request.get_another_path2() == '/'

    request.extend(get_third_path)
    assert request.get_third_path() == '/'

    request.extend(ExtendClass.get_another_path)
    assert request.get_another_path() == '/'

def test_gets_input_with_all_request_methods():
    app = App()
    app.bind('Request', REQUEST)
    request = app.make('Request').load_app(app)
    request.params = 'hey=test'

    request.environ['REQUEST_METHOD'] = 'GET'
    assert request.input('hey') == 'test'

    request.environ['REQUEST_METHOD'] = 'POST'
    assert request.input('hey') == 'test'

    request.environ['REQUEST_METHOD'] = 'PUT'
    assert request.input('hey') == 'test'

    request.environ['REQUEST_METHOD'] = 'PATCH'
    assert request.input('hey') == 'test'

    request.environ['REQUEST_METHOD'] = 'DELETE'
    assert request.input('hey') == 'test'

def test_hidden_form_request_method_changes_request_method():
    app = App()
    wsgi_request['QUERY_STRING'] = 'request_method=PUT'
    request_class = Request(wsgi_request)

    app.bind('Request', request_class)
    request = app.make('Request').load_app(app)

    assert request.environ['REQUEST_METHOD'] == 'PUT'


class MockWsgiInput():

    def read(self, value):
        return '{"id": 1}'


def test_get_json_input():
    json_wsgi = wsgi_request
    json_wsgi['REQUEST_METHOD'] = 'POST'
    json_wsgi['CONTENT_TYPE'] = 'application/json'
    json_wsgi['QUERY_STRING'] = ''
    json_wsgi['wsgi.input'] = MockWsgiInput()

    Route(json_wsgi)
    request_obj = Request(json_wsgi)

    assert isinstance(request_obj.params, dict)
    assert request_obj.input('payload') == {'id': 1}

