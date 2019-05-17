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
import unittest

class MockUser():

    __auth__ = 'email'
    password = '$2a$04$SXAMKoNuuiv7iO4g4U3ZOemyJJiKAHomUIFfGyH4hyo4LrLjcMqvS'
    users_password = 'pass123'
    email = 'user@email.com'
    name = 'testuser123'
    id = 1

    def where(self, column, name):
        return self

    def or_where(self, column, name):
        return self

    def first(self):
        return self

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


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.container = App()
        self.app = self.container
        view = View(self.container)
        self.request = Request(generate_wsgi())
        self.auth = Auth(self.request, MockUser())
        self.container.bind('View', view.render)
        self.container.bind('ViewClass', view)
        self.app.bind('Application', application)

    def reset_method(self):
        self.auth = Auth(self.request, MockUser())

    def test_auth(self):
        self.assertTrue(self.auth)

    def test_login_user(self):
        self.assertIsInstance(self.auth.login('user@email.com', 'secret'), MockUser)
        self.assertTrue(self.request.get_cookie('token'))

    def test_login_user_with_list_auth_column(self):
        user = MockUser
        user.__auth__ = ['email', 'name']
        self.assertIsInstance(self.auth.login('testuser123', 'secret'), user)
        self.assertTrue(self.request.get_cookie('token'))

    def test_get_user(self):
        self.assertTrue(self.auth.login_by_id(1))
        self.assertIsInstance(self.auth.user(), MockUser)

    def test_get_user_returns_false_if_not_loggedin(self):
        self.auth.login('user@email.com', 'wrong_secret')
        self.assertFalse(self.auth.user())

    def test_logout_user(self):
        self.assertIsInstance(self.auth.login('user@email.com', 'secret'), MockUser)
        self.assertTrue(self.request.get_cookie('token'))

        self.auth.logout()
        self.assertFalse(self.request.get_cookie('token'))
        self.assertFalse(self.auth.user())

    def test_login_user_fails(self):
        self.assertFalse(self.auth.login('user@email.com', 'bad_password'))

    def test_login_by_id(self):
        self.assertIsInstance(self.auth.login_by_id(1), MockUser)
        self.assertTrue(self.request.get_cookie('token'))

        self.assertFalse(self.auth.login_by_id(2))

    def test_login_once_does_not_set_cookie(self):
        self.assertIsInstance(self.auth.once().login_by_id(1), MockUser)
        self.assertIsNone(self.request.get_cookie('token'))

    def test_user_is_mustverify_instance(self):
        self.auth = Auth(self.request, MockVerifyUser())
        self.assertIsInstance(self.auth.once().login_by_id(1), MustVerifyEmail)
        self.reset_method()
        self.assertNotIsInstance(self.auth.once().login_by_id(1), MustVerifyEmail)

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

        self.assertEqual(response.rendered_template, 'confirm')

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

        self.assertEqual(response.rendered_template, 'error')
