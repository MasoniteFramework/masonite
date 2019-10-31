from src.masonite.auth.guards import WebGuard

from src.masonite.auth import Auth
from src.masonite.middleware import GuardMiddleware
from src.masonite.routes import Get
from src.masonite.testing import TestCase


class TestAuthMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.container.make(Auth).register_guard('api', Get)
        self.withRouteMiddleware({
            'guard': GuardMiddleware,
        })

        self.routes([
            Get('/guard/web', 'TestController@show').middleware('guard:web'),
            Get('/guard/api', 'TestController@show').middleware('guard:api')
        ])
    
    def test_can_switch_guards(self):
        self.get('/guard/web')
        self.assertIsInstance(self.container.make(Auth).get(), WebGuard)
        
        self.get('/guard/api')
        self.assertIsInstance(self.container.make(Auth).get(), Get)