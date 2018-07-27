from config import session
from masonite.app import App
from masonite.drivers.SessionCookieDriver import SessionCookieDriver
from masonite.drivers.SessionMemoryDriver import SessionMemoryDriver
from masonite.managers.SessionManager import SessionManager
from masonite.request import Request
from masonite.testsuite.TestSuite import generate_wsgi


class TestSession:

    def setup_method(self):
        wsgi_request = generate_wsgi()
        self.app = App()
        self.app.bind('Environ', wsgi_request)
        self.app.bind('Request', Request(wsgi_request))
        self.app.bind('SessionConfig', session)
        self.app.bind('SessionCookieDriver', SessionCookieDriver)
        self.app.bind('SessionMemoryDriver', SessionMemoryDriver)
        self.app.bind('SessionManager', SessionManager(self.app))
        self.app.bind('Application', self.app)


    def test_session_request(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session.set('username', 'pep')
            session.set('password', 'secret')
            assert session.get('username') == 'pep'
            assert session.get('password') == 'secret'


    def test_session_has_no_data(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session._session = {}
            session._flash = {}
            assert session.has('nodata') is False


    def test_change_ip_address(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session.environ['REMOTE_ADDR'] = '111.222.33.44'
            session.set('username', 'pep')
            assert session.get('username') == 'pep'


    def test_session_get_all_data(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session.environ['REMOTE_ADDR'] = 'get.all.data'
            session.set('username', 'pep')
            session.flash('password', 'secret')

            assert session.all() == {'username': 'pep', 'password': 'secret'}


    def test_session_has_data(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session._session = {}
            session._flash = {}
            session.set('username', 'pep')
            assert session.has('username') is True
            assert session.has('has_password') is False


    def test_session_helper(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session._session = {}
            session._flash = {}
            helper = session.helper

            assert isinstance(helper(), type(session))


    def test_session_flash_data(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session._session = {}
            session.flash('flash_username', 'pep')
            session.flash('flash_password', 'secret')
            assert session.get('flash_username') == 'pep'
            assert session.get('flash_password') == 'secret'


    def test_reset_flash_session_memory(self):
        session = self.app.make('SessionManager').driver('memory')
        session.flash('flash_', 'test_pep')
        session.reset(flash_only=True)
        assert session.get('flash_') is None


    def test_reset_flash_session_driver(self):
        session = self.app.make('SessionManager').driver('cookie')
        session.flash('flash_', 'test_pep')

        session.reset(flash_only=True)
        assert session.get('flash_') is None

    def test_session_flash_data_serializes_dict(self):
        for driver in ('cookie', 'memory'):
            session = self.app.make('SessionManager').driver(driver)
            session._session = {}
            session.flash('flash_dict', {'id': 1})
            session.set('get_dict', {'id': 1})
            assert session.get('flash_dict') == {'id': 1}
            assert session.get('get_dict') == {'id': 1}

    def test_reset_serializes_dict(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session.set('flash_', 'test_pep')
            session.reset()
            assert session.get('reset_username') is None

    def test_delete_session(self):
        for driver in ('memory', 'cookie'):
            session = self.app.make('SessionManager').driver(driver)
            session.set('test1', 'value')
            session.set('test2', 'value')
            assert session.delete('test1')
            assert session.has('test1') is False
            assert session.delete('test1') is False
