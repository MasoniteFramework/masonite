from routes import web
from src.masonite.testing import TestCase
from app.User import User
from src.masonite.exceptions import InvalidCSRFToken


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

        self.assertTrue(self.get('/unit/test/get').canView())

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
            self.get('/unit/test/get/params').isNamed('get.params')
        )

    def test_has_middleware(self):
        self.assertTrue(
            self.post('/unit/test/post').hasMiddleware('test')
        )

    def test_can_get_route_param(self):
        self.assertTrue(
            self.get('/unit/test/param/1').contains('1')
        )

    def test_can_have_user(self):

        self.assertTrue(
            self.actingAs(User.find(1)).post('/unit/test/user').contains('Joe')
        )

    def test_json(self):
        self.assertTrue(self.json('POST', '/unit/test/json', {'test': 'testing'}).contains('testing'))
    
    def test_json_response(self):
        self.assertTrue(self.json('GET', '/unit/test/json/response').hasJson('count', 5))

    def test_json_response_dictionary(self):
        self.assertTrue(self.json('GET', '/unit/test/json/response').hasJson({
            'count': 5
        }))
        
        self.assertFalse(self.json('GET', '/unit/test/json/response').hasJson({
            'count': 10
        }))

    def test_multi_json_response(self):
        self.assertTrue(self.json('GET', '/unit/test/json/multi').hasJson({
            'author.name': 'Joe'
        }))

        self.assertTrue(self.json('GET', '/unit/test/json/multi').hasJson('author.name', 'Joe'))
        self.assertFalse(self.json('GET', '/unit/test/json/multi_count').hasJson('count.foo', 'foo'))

    def test_as_dictionary(self):
        dictionary = self.json('GET', '/unit/test/json/multi').asDictionary()
        self.assertEqual(dictionary['author']['name'], 'Joe')

        with self.assertRaises(ValueError):
            dictionary = self.json('GET', '/login').asDictionary()

    def test_count(self):
        self.assertTrue(self.json('GET', '/unit/test/json/response').count(2))
        self.assertFalse(self.json('GET', '/unit/test/json/response').count(1))

        self.assertTrue(self.json('GET', '/unit/test/json/response').amount(2))
        self.assertFalse(self.json('GET', '/unit/test/json/response').amount(1))

    def test_has_amount(self):
        self.assertTrue(self.json('GET', '/unit/test/json/response').hasAmount('iterable', 3))
        self.assertFalse(self.json('GET', '/unit/test/json/response').hasAmount('iterable', 2))

        self.json('GET', '/unit/test/json/response').assertHasAmount('iterable', 3) 
        self.json('GET', '/unit/test/json/response').assertNotHasAmount('iterable', 2)

    def test_patch(self):
        self.assertTrue(self.patch('/unit/test/patch', {'test': 'testing'}).contains('testing'))

    def test_csrf(self):
        self.withCsrf()
        with self.assertRaises(InvalidCSRFToken):
            self.assertTrue(self.post('/unit/test/json', {'test': 'testing'}).contains('testing'))

    def test_database_has(self):
        self.assertDatabaseHas('users.email', 'user@example.com')
        self.assertDatabaseNotHas('users.email', 'joe@example.com')

    def test_acting_as_none(self):
        with self.assertRaises(TypeError):
            self.actingAs(User.find(10)).get('/helloworld')

    def test_capture_output(self):
        with self.captureOutput() as output:
            print('hello', end='')

        self.assertEqual(output.getvalue(), 'hello')
