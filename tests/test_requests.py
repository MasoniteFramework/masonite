from masonite.request import Request
from masonite.app import App
from masonite.routes import Get
from pydoc import locate
from config import application

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
    ''' Request should be callable '''
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
