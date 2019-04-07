import unittest

from app.http.controllers.TestController import \
    TestController as ControllerTest
from masonite.routes import Get
from masonite.testing import MockJson, MockRequest, UnitTest


class MockUser:
    admin = 0


class TestUnitTest(UnitTest, unittest.TestCase):

    def setUp(self):
        super().setup_method()

        self.routes([
            Get().route('/testing', 'TestController@show').name('testing.route').middleware('auth', 'owner')
        ])

    def test_unit_test_has_route(self):
        self.assertTrue(self.route('/testing'))
        self.assertFalse(self.route('/also/testing'))

    def test_unit_test_has_route_name(self):
        self.assertTrue(self.route('/testing').is_named('testing.route'))

    def test_unit_test_has_route_middleware(self):
        self.assertTrue(self.route('/testing').has_middleware('auth', 'owner'))
        self.assertTrue(self.route('/testing').has_middleware('auth'))
        self.assertFalse(self.route('/testing').has_middleware('auth', 'not'))

    def test_unit_test_has_controller(self):
        self.assertTrue(self.route('/testing').has_controller(ControllerTest))

    def test_user_can_be_loaded(self):
        self.assertTrue(self.route('/unit/test').user(MockUser).can_view())
        self.assertFalse(self.route('/unit/test').user(None).can_view())

    def test_view_contains(self):
        self.assertTrue(self.route('/test/route').contains('test'))
        self.assertTrue(self.route('/test/route').user(MockUser).contains('test'))

    def test_can_get_post_route(self):
        self.assertTrue(self.route('/test/post/route', method="POST").contains('post_test'))

    def test_can_get_status_code_with_post_method(self):
        route = self.route('/test/post/route', method="POST")
        self.assertTrue(route.status('200 OK'))
        self.assertTrue(route.ok())

    def test_get_returns_mock_request(self):
        self.assertIsInstance(self.get('/unit/1'), MockRequest)

    def test_can_get_status_code(self):
        self.assertTrue(self.get('/test/param/1').status('200 OK'))

    def test_route_is_post_request(self):
        self.assertTrue(self.route('/test/post/route', method="POST").is_post())

    def test_route_has_session(self):
        route = self.route('/test/set/test/session')
        self.assertTrue(route.has_session('test'))

        self.assertTrue(route.is_get())

        self.assertFalse(self.route('/test/set/test/session').has_session('not'))

    def test_route_finds_route_without_method(self):
        self.assertTrue(self.route('/test/post/route'))

    def test_json_returns_mock_json(self):
        self.assertIsInstance(self.json('POST', '/test/json/response/1', {'id': 1}), MockJson)

    def test_json_returns_200_OK(self):
        json = self.json('/test/json/response/1', {'id': 1}, method="POST")
        self.assertTrue(json.status('200 OK'))
        self.assertTrue(json.contains('success'))
