from masonite.request import Request
from masonite.auth.Sign import Sign
from cryptography.fernet import Fernet
from masonite.testsuite.TestSuite import generate_wsgi


class TestCookieSigning:

    def setup_method(self):
        self.secret_key = 'pK1tLuZA8-upZGz-NiSCP_UVt-fxpxd796TaG6-dp8Y='
        self.request = Request(generate_wsgi()).key(self.secret_key)

    def test_set_and_get_cookie(self):
        self.request.cookie('test', 'testvalue')
        assert self.request.get_cookie('test') == 'testvalue'

    def test_set_and_get_multiple_cookies(self):
        self.request.cookie('cookie1', 'cookie1value')
        self.request.cookie('cookie2', 'cookie2value')

        assert self.request.get_cookie('cookie1') == 'cookie1value'
        assert self.request.get_cookie('cookie2') == 'cookie2value'

    def test_set_cookie_without_encryption(self):
        self.request.cookie('notencrypted', 'value', False)

        assert self.request.get_cookie('notencrypted', False) == 'value'

    def test_set_and_get_cookie_with_no_existing_cookies(self):
        self.request.environ['HTTP_COOKIE'] = ''
        self.request.cookie('test', 'testvalue')
        assert self.request.get_cookie('test') == 'testvalue'

    def test_set_and_get_cookie_with_existing_cookie(self):
        self.request.environ['HTTP_COOKIE'] = 'cookie=true'
        self.request.cookie('test', 'testvalue')
        assert self.request.get_cookie('test') == 'testvalue'

    def test_set_and_get_cookie_with_http_only(self):
        self.request.cookies = []
        self.request.cookie('test', 'testvalue', encrypt=False)
        assert self.request.get_cookie('test', decrypt=False) == 'testvalue'
        assert 'HttpOnly' in self.request.cookies[0][1]
        assert 'test=testvalue; HttpOnly;Path=/' in self.request.cookies[0][1]

    def test_set_and_get_cookie_without_http_only(self):
        self.request.cookies = []
        self.request.cookie('test', 'testvalue', http_only=False, encrypt=False)
        assert self.request.get_cookie('test', decrypt=False) == 'testvalue'
        assert 'test=testvalue; Path=/' in self.request.cookies[0][1]
