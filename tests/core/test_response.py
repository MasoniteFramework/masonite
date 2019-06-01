import unittest

from orator import Model
from orator.support.collection import Collection

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

    def find(self, user_id):
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
