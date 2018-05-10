from config import session
from masonite.app import App
from masonite.drivers.SessionCookieDriver import SessionCookieDriver
from masonite.drivers.SessionMemoryDriver import SessionMemoryDriver
from masonite.managers.SessionManager import SessionManager
from masonite.request import Request


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


container = App()
container.bind('Environ', wsgi_request)
container.bind('Request', Request(wsgi_request))
container.bind('SessionConfig', session)
container.bind('SessionCookieDriver', SessionCookieDriver)
container.bind('SessionMemoryDriver', SessionMemoryDriver)
container.bind('SessionManager', SessionManager(container))
container.bind('Application', container)


def test_session_request():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION.set('username', 'pep')
        SESSION.set('password', 'secret')
        assert SESSION.get('username') == 'pep'
        assert SESSION.get('password') == 'secret'


def test_session_has_no_data():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION._session = {}
        SESSION._flash = {}
        assert SESSION.has('nodata') is False


def test_change_ip_address():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION.environ['REMOTE_ADDR'] = '111.222.33.44'
        SESSION.set('username', 'pep')
        assert SESSION.get('username') == 'pep'


def test_session_get_all_data():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION.environ['REMOTE_ADDR'] = 'get.all.data'
        SESSION.set('username', 'pep')
        SESSION.flash('password', 'secret')

        assert SESSION.all() == {'username': 'pep', 'password': 'secret'}


def test_session_has_data():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION._session = {}
        SESSION._flash = {}
        SESSION.set('username', 'pep')
        assert SESSION.has('username') is True
        assert SESSION.has('has_password') is False


def test_session_helper():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION._session = {}
        SESSION._flash = {}
        helper = SESSION.helper

        assert isinstance(helper(), type(SESSION))


def test_session_flash_data():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION._session = {}
        SESSION.flash('flash_username', 'pep')
        SESSION.flash('flash_password', 'secret')
        assert SESSION.get('flash_username') == 'pep'
        assert SESSION.get('flash_password') == 'secret'


def test_reset_flash_session_memory():
    SESSION = container.make('SessionManager').driver('memory')
    SESSION.flash('flash_', 'test_pep')
    SESSION.reset(flash_only=True)
    assert SESSION.get('flash_') is None


def test_reset_flash_session_driver():
    SESSION = container.make('SessionManager').driver('cookie')
    SESSION.flash('flash_', 'test_pep')

    SESSION.reset(flash_only=True)
    assert SESSION.get('flash_') is None


def test_reset_session():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION.set('flash_', 'test_pep')
        SESSION.reset()
        assert SESSION.get('reset_username') is None

def test_delete_session():
    for driver in ('memory', 'cookie'):
        SESSION = container.make('SessionManager').driver(driver)
        SESSION.set('test1', 'value')
        SESSION.set('test2', 'value')
        assert SESSION.delete('test1')
        assert SESSION.has('test1') is False
        assert SESSION.delete('test1') is False