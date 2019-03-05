import time
import datetime

from masonite.view import View
from masonite.auth import Auth
from masonite.request import Request
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.auth import MustVerifyEmail
from masonite.app import App
from masonite.auth import Sign
from masonite.helpers.routes import get
from masonite.snippets.auth.controllers.ConfirmController import ConfirmController
from config import application

from masonite.managers import AuthManager
from masonite.drivers import AuthCookieDriver, AuthJwtDriver


class MockUser():

    __auth__ = 'email'
    __primary_key__ = 'id'
    password = '$2a$04$SXAMKoNuuiv7iO4g4U3ZOemyJJiKAHomUIFfGyH4hyo4LrLjcMqvS'
    users_password = 'pass123'
    email = 'user@email.com'
    remember_token = '1234-56'
    name = 'testuser123'
    _found = False
    id = 1

    def serialize(self):
        return {
            'password': self.password,
            'email': self.email,
            'remember_token': self.remember_token,
            'name': self.name,
            '_found': self._found,
            'id': 1
        }
    
    def hydrate(self, dictionary):
        self.__dict__.update(dictionary)
        return self

    def where(self, column, name):
        if getattr(self, column) == name:
            self._found = True
        return self

    def or_where(self, column, name):
        if getattr(self, column) == name:
            self._found = True
        return self

    def first(self):
        if self._found == True:
            return self
        return False

    def save(self):
        pass

    def find(self, id):
        if self.id == id:
            return self
        return False


class MockVerifyUser(MockUser, MustVerifyEmail):
    verified_at = None
    pass


class ListUser(MockUser):
    __password__ = 'users_password'


class TestAuth:

    def setup_method(self):
        self.container = App()
        self.app = self.container
        view = View(self.container)
        self.request = Request(generate_wsgi()).load_app(self.app)
        self.auth = Auth(self.request, MockUser())
        self.container.bind('View', view.render)
        self.container.bind('ViewClass', view)
        self.app.bind('Application', application)

        self.app.bind('Request', self.request)
        self.app.bind('AuthCookieDriver', AuthCookieDriver)
        self.app.bind('AuthJwtDriver', AuthJwtDriver)
        self.app.bind('AuthManager', AuthManager(self.app).driver('cookie'))
        self.drivers = ('jwt', 'cookie')

    def reset_method(self):
        for driver in self.drivers:
            self.app.bind('AuthManager', AuthManager(self.app).driver(driver))
            self.auth = Auth(self.request, MockUser())

    def test_auth(self):
        assert self.auth

    def test_auth_gets_cookie_driver(self):
        assert isinstance(self.app.make('AuthManager'), AuthCookieDriver)

    def test_login_user(self):
        for driver in self.drivers:
            self.app.bind('AuthManager', AuthManager(self.app).driver(driver))
            assert isinstance(self.auth.login('user@email.com', 'secret'), MockUser)
            assert self.request.get_cookie('token')

    def test_login_user_with_list_auth_column(self):
        user = MockUser
        user.__auth__ = ['email', 'name']
        assert isinstance(self.auth.login('testuser123', 'secret'), user)
        assert self.request.get_cookie('token')

    def test_get_user(self):
        assert self.auth.login_by_id(1)
        assert isinstance(self.auth.user(), MockUser)

    def test_get_user_attributes(self):
        for driver in self.drivers:
            self.app.bind('AuthManager', AuthManager(self.app).driver(driver))
            assert self.auth.login_by_id(1)
            assert self.auth.user().id == 1
            assert not hasattr(self.auth.auth_model, 'expired')

    def test_get_user_returns_false_if_not_loggedin(self):
        self.auth.login('user@email.com', 'wrong_secret')
        assert self.auth.user() is False

    def test_logout_user(self):
        assert isinstance(self.auth.login('user@email.com', 'secret'), MockUser)
        assert self.request.get_cookie('token')

        self.auth.logout()
        assert not self.request.get_cookie('token')
        assert not self.auth.user()

    def test_login_user_fails(self):
        assert self.auth.login('user@email.com', 'bad_password') is False

    def test_login_by_id(self):
        assert isinstance(self.auth.login_by_id(1), MockUser)
        assert self.request.get_cookie('token')

        assert self.auth.login_by_id(2) is False

    def test_login_once_does_not_set_cookie(self):
        assert isinstance(self.auth.once().login_by_id(1), MockUser)
        assert self.request.get_cookie('token') is None

    def test_user_is_mustverify_instance(self):
        self.auth = Auth(self.request, MockVerifyUser())
        assert isinstance(self.auth.once().login_by_id(1), MustVerifyEmail)
        self.reset_method()
        assert not isinstance(self.auth.once().login_by_id(1), MustVerifyEmail)

    def get_user(self, id):
        return MockVerifyUser()

    def test_confirm_controller_success(self):
        self.auth = Auth(self.request, MockVerifyUser())
        params = {'id': Sign().sign('{0}::{1}'.format(1, time.time()))}
        self.request.set_params(params)
        user = self.auth.once().login_by_id(1)
        self.request.set_user(user)

        self.app.bind('Request', self.request)
        self.app.make('Request').load_app(self.app)

        # Create the route
        route = get('/email/verify/@id', ConfirmController.confirm_email)

        ConfirmController.get_user = self.get_user

        # Resolve the controller constructor
        controller = self.app.resolve(route.controller)

        # Resolve the method
        response = self.app.resolve(getattr(controller, route.controller_method))
        self.reset_method()

        assert response.rendered_template == 'confirm'

    def test_confirm_controller_failure(self):
        self.auth = Auth(self.request, MockVerifyUser())

        timestamp_plus_11 = datetime.datetime.now() - datetime.timedelta(minutes=11)

        params = {'id': Sign().sign('{0}::{1}'.format(1, timestamp_plus_11.timestamp()))}
        self.request.set_params(params)
        user = self.auth.once().login_by_id(1)
        self.request.set_user(user)

        self.app.bind('Request', self.request)
        self.app.make('Request').load_app(self.app)

        # Create the route
        route = get('/email/verify/@id', ConfirmController.confirm_email)

        ConfirmController.get_user = self.get_user

        # Resolve the controller constructor
        controller = self.app.resolve(route.controller)

        # Resolve the method
        response = self.app.resolve(getattr(controller, route.controller_method))
        self.reset_method()

        assert response.rendered_template == 'error'
