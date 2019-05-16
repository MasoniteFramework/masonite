from masonite.request import Request
from masonite.auth.Sign import Sign
from cryptography.fernet import Fernet
from masonite.testsuite.TestSuite import generate_wsgi
import unittest

class TestCookieSigning(unittest.TestCase):

    def setUp(self):
        self.secret_key = 'pK1tLuZA8-upZGz-NiSCP_UVt-fxpxd796TaG6-dp8Y='
        self.request = Request(generate_wsgi()).key(self.secret_key)

    def test_set_and_get_cookie(self):
        self.request.cookie('test', 'testvalue')
        self.assertEqual(self.request.get_cookie('test'), 'testvalue')

    def test_set_and_get_multiple_cookies(self):
        self.request.cookie('cookie1', 'cookie1value')
        self.request.cookie('cookie2', 'cookie2value')

        self.assertEqual(self.request.get_cookie('cookie1'), 'cookie1value')
        self.assertEqual(self.request.get_cookie('cookie2'), 'cookie2value')

    def test_set_cookie_without_encryption(self):
        self.request.cookie('notencrypted', 'value', False)

        self.assertEqual(self.request.get_cookie('notencrypted', False), 'value')

    def test_set_and_get_cookie_with_no_existing_cookies(self):
        self.request.environ['HTTP_COOKIE'] = ''
        self.request.cookie('test', 'testvalue')
        self.assertEqual(self.request.get_cookie('test'), 'testvalue')

    def test_set_and_get_cookie_with_existing_cookie(self):
        self.request.environ['HTTP_COOKIE'] = 'cookie=true'
        self.request.cookie('test', 'testvalue')
        self.assertEqual(self.request.get_cookie('test'), 'testvalue')

    def test_set_and_get_cookie_with_http_only(self):
        self.request.cookies = []
        self.request.cookie('test', 'testvalue', encrypt=False)
        self.assertEqual(self.request.get_cookie('test', decrypt=False), 'testvalue')
        self.assertTrue(self.request.get_raw_cookie('test')['httponly'])
        self.assertIn('/', self.request.get_raw_cookie('test')['path'])
        self.assertIn('testvalue', self.request.get_raw_cookie('test').value)

    def test_set_and_get_cookie_without_http_only(self):
        self.request.cookies = []
        self.request.cookie('test', 'testvalue', http_only=False, encrypt=False)
        self.assertEqual(self.request.get_cookie('test', decrypt=False), 'testvalue')
        self.assertIn('/', self.request.get_raw_cookie('test')['path'])
        self.assertIn('testvalue', self.request.get_raw_cookie('test').value)
