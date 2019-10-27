
from orator import LengthAwarePaginator, Model, Paginator
from orator.support.collection import Collection

from app.http.controllers.TestController import \
    TestController as ControllerTest
from app.User import User
from config.factories import factory
from src.masonite.response import Response
from src.masonite.routes import Get
from src.masonite.testing import TestCase
from src.masonite.view import View


class MockUser(Model):
    __table__ = 'users'

    def all(self):
        return Collection([
            {'name': 'TestUser', 'email': 'user@email.com'},
            {'name': 'TestUser', 'email': 'user@email.com'}
        ])

    def find(self, _):
        self.name = 'TestUser'
        self.email = 'user@email.com'
        return self

class MockController:

    def test_json(self, response: Response):
        return response.json({'test': 'value'})

    def redirect(self, response: Response):
        return response.redirect('/some/test')

    def view(self, view: View):
        return view.render('test', {'test': 'test'})

    def response_int(self, response: Response):
        return response.view(1)

    def all_users(self):
        return MockUser().all()

    def paginate(self):
        return MockUser.paginate(10)

    def single(self):
        return User.find(1)

    def length_aware(self):
        return LengthAwarePaginator(User.find(1), 1, 10)

    def paginator(self):
        return Paginator(User.all(), 10)

    def single_paginator(self):
        return Paginator(User.find(1), 10)


class TestResponse(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(only=[
            Get('/json', MockController.test_json),
            Get('/redirect', MockController.redirect),
            Get('/change/header', ControllerTest.change_header),
            Get('/view', MockController.view),
            Get('/int', MockController.response_int),
            Get('/404', ControllerTest.change_404),
            Get('/change/status', ControllerTest.change_status),
            Get('/users', MockController.all_users),
            Get('/paginate', MockController.paginate),
            Get('/paginator', MockController.paginator),
            Get('/single_paginator', MockController.single_paginator),
            Get('/single', MockController.single),
            Get('/length_aware', MockController.length_aware),
        ])
    
    def setUpFactories(self):
        factory(User, 50).create()

    def test_can_set_json(self):
        (
            self.json('GET', '/json')
                .assertIsStatus(200)
                .assertHeaderIs('Content-Length', 17)
                .assertHeaderIs('Content-Type', 'application/json; charset=utf-8')
        )

    def test_redirect(self):
        (
            self.get('/redirect')
                .assertHeaderIs('Location', '/some/test')
                .assertIsStatus(302)
        )

    def test_response_does_not_override_header_from_controller(self):
        (
            self.get('/change/header')
                .assertHeaderIs('Content-Type', 'application/xml')
        )

    def test_view(self):
        (
            self.get('/view')
                .assertContains('test')
                .assertIsStatus(200)
        )

    def test_view_can_return_integer_as_string(self):
        (
            self.get('/int')
                .assertContains('1')
                .assertIsStatus(200)
        )

    def test_view_can_set_own_status_code_to_404(self):
        (
            self.get('/404')
                .assertNotFound()
        )

    def test_view_can_set_own_status_code(self):
        (
            self.get('/change/status')
                .assertIsStatus(203)
        )

    def test_view_should_return_a_json_response_when_retrieve_a_user_from_model(self):
        (
            self.json('GET', '/users')
                .assertCount(2)
                .assertJsonContains('name', 'TestUser')
                .assertJsonContains('email', 'user@email.com')
        )


    def test_view_should_return_a_json_response_when_returning_length_aware_paginator_instance(self):

        users = User.all()

        # Page 1
        (
            self.get('/paginate')
                .assertHasJson('total', len(users))
                .assertHasJson('count', 10)
                .assertHasJson('per_page', 10)
                .assertHasJson('current_page', 1)
                .assertHasJson('from', 1)
                .assertHasJson('to', 10)
        )

        # Page 2
        (
            self.get('/paginate', {'page': 2})
                .assertHasJson('total', len(users))
                .assertHasJson('count', 10)
                .assertHasJson('per_page', 10)
                .assertHasJson('current_page', 2)
                .assertHasJson('from', 11)
                .assertHasJson('to', 20)
        )

        factory(User).create()
        (
            self.get('/length_aware')
                .assertHasJson('total', 1)
                .assertHasJson('count', 1)
        )


    def test_view_should_return_a_json_response_when_returning_paginator_instance(self):
        
        (
            self.get('/paginator')
                .assertHasJson('count', 10)
                .assertHasJson('per_page', 10)
                .assertHasJson('current_page', 1)
                .assertHasJson('from', 1)
                .assertHasJson('to', 10)
        )


    def test_can_correct_incorrect_pagination_page(self):
        users = User.all()
        (
            self.get('/paginator')
                .assertHasJson('count', 10)
                .assertHasJson('per_page', 10)
                .assertHasJson('current_page', 1)
                .assertHasJson('from', 1)
                .assertHasJson('to', 10)
        )
        
        (self.get('/paginate', {'page': 'hey', 'page_size': 'hey'})
                .assertHasJson('total', len(users))
                .assertHasJson('count', 10)
                .assertHasJson('per_page', 10)
                .assertHasJson('current_page', 1)
                .assertHasJson('from', 1)
                .assertHasJson('to', 10))

        (self.get('/length_aware', {'page': 'hey', 'page_size': 'hey'})
                # .assertHasJson('total', len(User.find(1)))
                # .assertHasJson('count', len(User.find(1)))
                .assertHasJson('per_page', 10)
                .assertHasJson('current_page', 1)
                .assertHasJson('from', 1)
                .assertHasJson('to', 10))

        (self.get('/single_paginator', {'page': 'hey', 'page_size': 'hey'})
                .assertHasJson('count', 1)
                .assertHasJson('per_page', 10)
                .assertHasJson('current_page', 1)
                .assertHasJson('from', 1)
                .assertHasJson('to', 10))
