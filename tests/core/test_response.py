import unittest
import json

from orator import Model
from orator.support.collection import Collection
from orator import Paginator, LengthAwarePaginator

from app.http.controllers.TestController import \
    TestController as ControllerTest
from masonite.app import App
from masonite.request import Request
from masonite.response import Response
from masonite.testsuite import generate_wsgi
from masonite.view import View


class MockUser(Model):

    def all(self):
        return Collection([
            {'name': 'TestUser', 'email': 'user@email.com'},
            {'name': 'TestUser', 'email': 'user@email.com'}
        ])

    def find(self, _):
        self.name = 'TestUser'
        self.email = 'user@email.com'
        return self


class TestResponse(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.request = Request(generate_wsgi()).load_app(self.app)
        self.app.bind('Request', self.request)
        self.app.bind('StatusCode', None)
        self.response = Response(self.app)
        self.app.bind('Response', self.response)

    def test_can_set_json(self):
        self.response.json({'test': 'value'})

        self.assertTrue(self.request.is_status(200))
        self.assertEqual(self.request.header('Content-Length'), '17')
        self.assertEqual(self.request.header('Content-Type'), 'application/json; charset=utf-8')

    def test_redirect(self):
        self.response.redirect('/some/test')

        self.request.header('Location', '/some/test')
        self.assertTrue(self.request.is_status(302))
        self.assertEqual(self.request.header('Location'), '/some/test')

    def test_response_does_not_override_header_from_controller(self):
        self.response.view(self.app.resolve(ControllerTest().change_header))

        self.assertEqual(self.request.header('Content-Type'), 'application/xml')

    def test_view(self):
        view = View(self.app).render('test', {'test': 'test'})

        self.response.view(view)

        self.assertEqual(self.app.make('Response'), 'test')
        self.assertTrue(self.request.is_status(200))

        self.response.view('foobar')

        self.assertEqual(self.app.make('Response'), 'foobar')

    def test_view_can_return_integer_as_string(self):
        self.response.view(1)

        self.assertEqual(self.app.make('Response'), '1')
        self.assertTrue(self.request.is_status(200))

    def test_view_can_set_own_status_code_to_404(self):
        self.response.view(self.app.resolve(ControllerTest().change_404))
        self.assertTrue(self.request.is_status(404))

    def test_view_can_set_own_status_code(self):

        self.response.view(self.app.resolve(ControllerTest().change_status))
        self.assertTrue(self.request.is_status(203))

    def test_view_should_return_a_json_response_when_retrieve_a_user_from_model(self):

        self.assertIsInstance(MockUser(), Model)
        self.response.view(MockUser().all())

        self.assertIn('"name": "TestUser"', self.app.make('Response'))
        self.assertIn('"email": "user@email.com"', self.app.make('Response'))

        self.response.view(MockUser().find(1))

        self.assertIn('"name": "TestUser"', self.app.make('Response'))
        self.assertIn('"email": "user@email.com"', self.app.make('Response'))

    def test_view_should_return_a_json_response_when_returning_length_aware_paginator_instance(self):

        self.assertIsInstance(MockUser(), Model)
        users = MockUser().all()
        num_users = len(users)
        page_size = 15
        self.response.view(LengthAwarePaginator(users, num_users, page_size))

        self.assertIn('"total": {}'.format(num_users), self.app.make('Response'))
        self.assertIn('"count": {}'.format(num_users), self.app.make('Response'))
        self.assertIn('"per_page": {}'.format(page_size), self.app.make('Response'))
        self.assertIn('"current_page": 1', self.app.make('Response'))
        self.assertIn('"last_page": 1', self.app.make('Response'))
        self.assertIn('"from": 1', self.app.make('Response'))
        self.assertIn('"to": {}'.format(page_size), self.app.make('Response'))
        self.assertIn('"data": ', self.app.make('Response'))
        self.assertIn(
            {'name': 'TestUser', 'email': 'user@email.com'},
            json.loads(self.app.make('Response'))['data']
        )

        users = [MockUser().find(1)]
        num_users = len(users)
        default_page_size = 15
        page_size_param = 10
        self.request._set_standardized_request_variables({'page_size': str(page_size_param)})
        self.response.view(LengthAwarePaginator(users, num_users, default_page_size))

        self.assertIn('"total": {}'.format(num_users), self.app.make('Response'))
        self.assertIn('"count": {}'.format(num_users), self.app.make('Response'))
        self.assertIn('"per_page": {}'.format(page_size_param), self.app.make('Response'))
        self.assertIn('"current_page": 1', self.app.make('Response'))
        self.assertIn('"last_page": 1', self.app.make('Response'))
        self.assertIn('"from": 1', self.app.make('Response'))
        self.assertIn('"to": {}'.format(page_size_param), self.app.make('Response'))
        self.assertIn('"data": ', self.app.make('Response'))
        self.assertIn(
            {'name': 'TestUser', 'email': 'user@email.com'},
            json.loads(self.app.make('Response'))['data']
        )

    def test_view_should_return_a_json_response_when_returning_paginator_instance(self):

        self.assertIsInstance(MockUser(), Model)
        users = MockUser().all()
        num_users = len(users)
        page_size = 15
        self.response.view(Paginator(users, page_size))

        self.assertIn('"count": {}'.format(num_users), self.app.make('Response'))
        self.assertIn('"per_page": {}'.format(page_size), self.app.make('Response'))
        self.assertIn('"current_page": 1', self.app.make('Response'))
        self.assertIn('"from": 1', self.app.make('Response'))
        self.assertIn('"to": {}'.format(page_size), self.app.make('Response'))
        self.assertIn('"data": ', self.app.make('Response'))
        self.assertIn(
            {'name': 'TestUser', 'email': 'user@email.com'},
            json.loads(self.app.make('Response'))['data']
        )

        users = [MockUser().find(1)]
        num_users = len(users)
        default_page_size = 15
        page_size_param = 10
        self.request._set_standardized_request_variables({'page_size': str(page_size_param)})
        self.response.view(Paginator(users, default_page_size))

        self.assertIn('"count": {}'.format(num_users), self.app.make('Response'))
        self.assertIn('"per_page": {}'.format(page_size_param), self.app.make('Response'))
        self.assertIn('"current_page": 1', self.app.make('Response'))
        self.assertIn('"from": 1', self.app.make('Response'))
        self.assertIn('"to": {}'.format(page_size_param), self.app.make('Response'))
        self.assertIn('"data": ', self.app.make('Response'))
        self.assertIn(
            {'name': 'TestUser', 'email': 'user@email.com'},
            json.loads(self.app.make('Response'))['data']
        )
