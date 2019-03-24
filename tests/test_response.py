from masonite.request import Request
from masonite.testsuite import generate_wsgi
from masonite.response import Response
from masonite.view import View
from masonite.app import App
from app.http.controllers.TestController import TestController as ControllerTest

from orator import Model
from orator.support.collection import Collection

class MockUser(Model):



    def all(self):
        return Collection([
            {'name': 'TestUser', 'email': 'user@email.com'},
            {'name': 'TestUser', 'email': 'user@email.com'}
        ])

    def find(self, id):
        self.name = 'TestUser'
        self.email = 'user@email.com'
        return self


class TestResponse:

    def setup_method(self):
        self.app = App()
        self.request = Request(generate_wsgi()).load_app(self.app)
        self.app.bind('Request', self.request)
        self.app.bind('StatusCode', None)
        self.response = Response(self.app)
        self.app.bind('Response', self.response)

    def test_can_set_json(self):
        self.response.json({'test': 'value'})

        assert self.request.is_status(200)
        assert self.request.header('Content-Length') == '17'
        assert self.request.header('Content-Type') == 'application/json; charset=utf-8'
    
    def test_redirect(self):
        self.response.redirect('/some/test')

        assert self.request.is_status(302)
        assert self.request.header('Location', '/some/test')

    def test_response_does_not_override_header_from_controller(self):
        self.response.view(self.app.resolve(ControllerTest().change_header))

        assert self.request.header('Content-Type') == 'application/xml'
    
    def test_view(self):
        view = View(self.app).render('test', {'test': 'test'})

        self.response.view(view)

        assert self.app.make('Response') == 'test'
        assert self.request.is_status(200)

        self.response.view('foobar')

        assert self.app.make('Response') == 'foobar'

    def test_view_can_return_integer_as_string(self):
        self.response.view(1)

        assert self.app.make('Response') == '1'
        assert self.request.is_status(200)

    def test_view_can_set_own_status_code_to_404(self):
        self.response.view(self.app.resolve(ControllerTest().change_404))
        assert self.request.is_status(404)

    def test_view_can_set_own_status_code(self):

        self.response.view(self.app.resolve(ControllerTest().change_status))
        assert self.request.is_status(203)


    def test_view_should_return_a_json_response_when_retrieve_a_user_from_model(self):
        
        assert isinstance(MockUser(), Model)
        self.response.view(MockUser().all())

        assert '"name": "TestUser"' in self.app.make('Response')
        assert '"email": "user@email.com"' in self.app.make('Response')

        self.response.view(MockUser().find(1))

        assert '"name": "TestUser"' in self.app.make('Response')
        assert '"email": "user@email.com"' in self.app.make('Response')

