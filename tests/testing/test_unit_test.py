from masonite.testing import UnitTest, MockRequest
from masonite.routes import Get
from app.http.controllers.TestController import TestController as ControllerTest

class MockUser:
    admin = 0

class TestUnitTest(UnitTest):

    def setup_method(self):
        super().setup_method()

        self.routes([
            Get().route('/testing', 'TestController@show').name('testing.route').middleware('auth', 'owner')
        ])

    def test_unit_test_has_route(self):
        assert self.route('/testing') 
        assert not self.route('/also/testing')

    def test_unit_test_has_route_name(self):
        assert self.route('/testing').is_named('testing.route')

    def test_unit_test_has_route_middleware(self):
        assert self.route('/testing').has_middleware('auth', 'owner')
        assert self.route('/testing').has_middleware('auth')
        assert not self.route('/testing').has_middleware('auth', 'not')

    def test_unit_test_has_route_middleware(self):
        assert self.route('/testing').has_controller(ControllerTest)

    def test_user_can_be_loaded(self):
        assert not self.route('/unit/test').user(None).can_view()
        assert self.route('/unit/test').user(MockUser).can_view()

    def test_view_contains(self):
        assert self.route('/test/route').contains('test')
        assert self.route('/test/route').user(MockUser).contains('test')

    def test_can_get_post_route(self):
        assert self.route('/test/post/route', method="POST").contains('post_test')

    def test_can_get_status_code(self):
        route = self.route('/test/post/route', method="POST")
        assert route.status('200 OK')

    def test_get_returns_mock_request(self):
        assert isinstance(self.get('/unit/1'), MockRequest)

    def test_can_get_status_code(self):
        assert self.get('/test/param/1').status('200 OK')
