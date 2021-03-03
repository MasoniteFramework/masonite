from src.masonite.middleware import CorsMiddleware
from src.masonite.routes import Get
from src.masonite.testing import TestCase

class TestCorsMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.buildOwnContainer()
        self.middleware = CorsMiddleware
        self.middleware.CORS = {"Access-Control-Allow-Origin": "*"}
        self.withHttpMiddleware([
            self.middleware,
        ])
        self.routes(only=[
            Get('/', 'TestController@show'),
        ])

    def test_cors_middleware(self):
        mock = self.get('/')
        mock.assertHeaderIs('Access-Control-Allow-Origin', '*')
