
from src.masonite.drivers import SessionCookieDriver, SessionMemoryDriver
from src.masonite.managers import SessionManager
from src.masonite.testing import generate_wsgi, TestCase

class TestSession(TestCase):

    def setUp(self):
        super().setUp()
        self.container.make('Request').load_environ(generate_wsgi())
        self.container.bind('SessionMemoryDriver', SessionMemoryDriver)
        self.container.bind('SessionCookieDriver', SessionCookieDriver)
        self.container.bind('SessionManager', SessionManager(self.container))

    def test_session_request(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session.set('username', 'pep')
            session.set('password', 'secret')
            self.assertEqual(session.get('username'), 'pep')
            self.assertEqual(session.get('password'), 'secret')

    def test_session_has_no_data(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session._session = {}
            session._flash = {}
            self.assertFalse(session.has('nodata'))

    def test_change_ip_address(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session.request.environ['REMOTE_ADDR'] = '111.222.33.44'
            session.set('username', 'pep')
            self.assertEqual(session.get('username'), 'pep')

    def test_session_get_all_data(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session.request.environ['REMOTE_ADDR'] = 'get.all.data'
            session.set('username', 'pep')
            session.flash('password', 'secret')

            self.assertEqual(session.all(), {'username': 'pep', 'password': 'secret'})

    def test_session_has_data(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session._session = {}
            session._flash = {}
            session.set('username', 'pep')
            self.assertTrue(session.has('username'))
            self.assertFalse(session.has('has_password'))

    def test_session_helper(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session._session = {}
            session._flash = {}
            helper = session.helper

            self.assertIsInstance(helper(), type(session))

    def test_session_flash_data(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session._session = {}
            session.flash('flash_username', 'pep')
            session.flash('flash_password', 'secret')
            self.assertEqual(session.get('flash_username'), 'pep')
            self.assertEqual(session.get('flash_password'), 'secret')

    def test_reset_flash_session_memory(self):
        session = self.container.make('SessionManager').driver('memory')
        session.flash('flash_', 'test_pep')
        session.reset(flash_only=True)
        self.assertIsNone(session.get('flash_'))

    def test_reset_flash_session_driver(self):
        session = self.container.make('SessionManager').driver('cookie')
        session.flash('flash_', 'test_pep')

        session.reset(flash_only=True)
        self.assertIsNone(session.get('flash_'))

    def test_session_flash_data_serializes_dict(self):
        for driver in ('cookie', 'memory'):
            session = self.container.make('SessionManager').driver(driver)
            session._session = {}
            session.flash('flash_dict', {'id': 1})
            session.set('get_dict', {'id': 1})
            self.assertEqual(session.get('flash_dict'), {'id': 1})
            self.assertEqual(session.get('get_dict'), {'id': 1})

    def test_session_flash_data_serializes_list(self):
        for driver in ('cookie', 'memory'):
            session = self.container.make('SessionManager').driver(driver)
            session._session = {}
            session.flash('flash_dict', [1, 2, 3])
            self.assertEqual(session.get('flash_dict'), [1, 2, 3])

    def test_reset_serializes_dict(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session.set('flash_', 'test_pep')
            session.reset()
            self.assertIsNone(session.get('reset_username'))

    def test_delete_session(self):
        for driver in ('memory', 'cookie'):
            session = self.container.make('SessionManager').driver(driver)
            session.set('test1', 'value')
            session.set('test2', 'value')
            self.assertTrue(session.delete('test1'))
            self.assertFalse(session.has('test1'))
            self.assertFalse(session.delete('test1'))

    def test_can_redirect_with_inputs(self):
        for driver in ('memory', 'cookie'):
            request = self.container.make('Request')
            request.request_variables = {
                'key1': 'val1',
                'key2': 'val2',
            }
            request.with_input()
            session = self.container.make('SessionManager').driver(driver)
            self.assertFalse(session.has('key1'))
            self.assertFalse(session.has('key2'))
