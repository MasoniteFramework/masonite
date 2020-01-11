
import unittest

from src.masonite.app import App
from src.masonite.providers import HelpersProvider
from src.masonite.request import Request
from src.masonite.testing import generate_wsgi
from src.masonite.view import View


class TestViewHelpers(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.view = View(self.app)
        self.request = Request(generate_wsgi()).load_app(self.app)
        self.provider = HelpersProvider()
        self.provider.load_app(self.app).boot(self.view, self.request)

    def test_boot_added_view_shares(self):
        self.assertGreater(len(self.view._shared), 1)

    def test_request_view_helper_is_view_class(self):
        self.assertIsInstance(self.view._shared['request'](), Request)

    def test_auth_returns_user_and_none(self):
        self.assertIsNone(self.view._shared['auth']())
        self.request.set_user(MockUser)
        self.assertEqual(self.view._shared['auth']().id, 1)

    def test_request_method_returns_hidden_input(self):
        self.assertEqual(self.view._shared['request_method']('PUT'), "<input type='hidden' name='__method' value='PUT'>")

    def test_can_sign_and_encrypt(self):
        self.assertNotEqual(self.view._shared['sign']('secret'), 'secret')
        self.assertGreater(len(self.view._shared['sign']('secret')), 10)

        self.assertNotEqual(self.view._shared['encrypt']('secret'), 'secret')
        self.assertGreater(len(self.view._shared['encrypt']('secret')), 10)

    def test_can_unsign_and_decrypt(self):
        signed = self.view._shared['sign']('secret')
        self.assertEqual(self.view._shared['decrypt'](signed), 'secret')
        self.assertEqual(self.view._shared['unsign'](signed), 'secret')

    def test_can_get_config(self):
        self.assertEqual(self.view._shared['config']('cache.driver'), 'disk')

    def test_optional(self):
        self.assertEqual(self.view._shared['optional'](MockUser).id, 1)
        self.assertNotEqual(self.view._shared['optional'](MockUser).test, 1)

    def test_cookie(self):
        self.request.cookie('test', 'value')
        self.assertEqual(self.view._shared['cookie']('test'), 'value')

    def test_hidden(self):
        self.assertEqual(self.view._shared['hidden']('test', name='form1'), "<input type='hidden' name='form1' value='test'>")


class MockUser:
    id = 1
