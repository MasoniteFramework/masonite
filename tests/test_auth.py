from masonite.facades.Auth import Auth
from masonite.request import Request
from masonite.testsuite.TestSuite import generate_wsgi

class MockUser():

    __auth__ = 'email'
    password = '$2a$04$SXAMKoNuuiv7iO4g4U3ZOemyJJiKAHomUIFfGyH4hyo4LrLjcMqvS'
    email = 'user@email.com'

    def where(self, column, name):
        return self

    def first(self):
        return self
    
    def save(self):
        pass
    
    def find(self, id):
        return self

class TestAuth:

    def setup_method(self):
        self.request = Request(generate_wsgi())

        self.auth = Auth(self.request, MockUser())

    def test_auth(self):
        assert self.auth
    
    def test_login_user(self):
        assert isinstance(self.auth.login('user@email.com', 'secret'), MockUser)
        assert self.request.get_cookie('token')
    
    def test_login_user_fails(self):
        assert self.auth.login('user@email.com', 'bad_password') is False
    
    def test_login_by_id(self):
        assert isinstance(self.auth.login_by_id(1), MockUser)
        assert self.request.get_cookie('token')
    
    def test_login_once_does_not_set_cookie(self):
        assert isinstance(self.auth.once().login_by_id(1), MockUser)
        assert self.request.get_cookie('token') is None
