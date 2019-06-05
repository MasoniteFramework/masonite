from routes import web
from masonite.testing import TestCase
from app.User import User


class TestUnitTest(TestCase):

    def setUp(self):
        super().setUp()

        self.routes(web.ROUTES)
    
    def setUpFactories(self):
        User.create({
            'name': 'Joe',
            'email': 'user@example.com',
            'password': 'secret'
        })

    def test_can_get_route(self):
        self.assertTrue(self.get('/unit/test/get').ok())

    def test_can_post_route(self):
        self.assertTrue(self.post('/unit/test/post').ok())
        self.assertTrue(self.post('/unit/test/post').contains('posted'))

    def test_can_send_post_parameters(self):
        self.assertTrue(
            self.post('/unit/test/params', {'test': 'test this'}).contains('test this')
        )

    def test_can_send_get_parameters(self):
        self.assertTrue(
            self.get('/unit/test/get/params', {'test': 'test this'}).contains('test this')
        )

    def test_can_test_route_name(self):
        self.assertTrue(
            self.get('/unit/test/get/params').is_named('get.params')
        )

    def test_has_middleware(self):
        self.assertTrue(
            self.post('/unit/test/post').has_middleware('test')
        )

    def test_can_have_user(self):
        self.assertTrue(
            self.acting_as(User.find(1)).post('/unit/test/user').contains('Joe')
        )
