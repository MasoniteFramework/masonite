from masonite.request import Request
from masonite.testsuite import generate_wsgi
from masonite.response import Response
from masonite.view import View
from masonite.app import App
from app.http.controllers.TestController import TestController as ControllerTest

class TestResponse:

    def setup_method(self):
        self.app = App()
        self.request = Request(generate_wsgi()).load_app(self.app)
        self.app.bind('Request', self.request)
        self.response = Response(self.app)
    
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
