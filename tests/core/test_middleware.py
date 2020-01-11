from src.masonite.request import Request
from src.masonite.routes import Get
from app.http.middleware.TestMiddleware import TestMiddleware as MiddlewareTest
from app.http.middleware.TestHttpMiddleware import TestHttpMiddleware as MiddlewareHttpTest
from src.masonite.testing import TestCase


class MiddlewareValueTest:

    def __init__(self, request: Request):
        self.request = request

    def before(self, value1, value2):
        self.request.value1 = value1
        self.request.value2 = value2

class ParameterMiddleware:

    def __init__(self, request: Request):
        self.request = request

    def before(self, value1):
        self.request.value1 = value1


class TestMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(only=[
            Get().route('/', 'TestController@show').middleware('test'),
            Get().route('/test', 'TestController@show').middleware('throttle:1,2'),
            Get().route('/test/@param', 'TestController@show').middleware('params:@param'),
        ])

        self.withRouteMiddleware({
            'test': MiddlewareTest,
            'throttle': MiddlewareValueTest,
            'params': ParameterMiddleware,
        }).withHttpMiddleware([MiddlewareHttpTest])

    def test_route_middleware_runs(self):
        self.get('/').assertPathIs('/test/middleware')

    def test_http_middleware_runs(self):
        self.get('/').assertPathIs('/test/middleware')
        self.assertEqual(self.get('/').request.environ['HTTP_TEST'], 'test')

    def test_route_middleware_can_pass_values(self):
        self.assertEqual(self.get('/test').request.value1, '1')
        self.assertEqual(self.get('/test').request.value2, '2')

    def test_route_middleware_get_parameters(self):
        request = self.get('/test/slug').request
        self.assertEqual(request.value1, 'slug')
