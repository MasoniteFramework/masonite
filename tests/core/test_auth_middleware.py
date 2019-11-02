from src.masonite.auth.guards import WebGuard

from src.masonite.auth import Auth
from src.masonite.middleware import GuardMiddleware
from src.masonite.routes import Get
from src.masonite.testing import TestCase

class MockApiGuard:

    def user(self):
        return 'user'

class MockController:

    def user(self, auth: Auth):
        return auth.user()

class TestAuthMiddleware(TestCase):

    def setUp(self):
        super().setUp()
        self.container.make(Auth).register_guard('api', MockApiGuard)

        self.withRouteMiddleware({
            'guard': GuardMiddleware,
        })

        self.routes([
            Get('/guard/web', MockController.user).middleware('guard:web'),
            Get('/guard/api', MockController.user).middleware('guard:api')
        ]) 
    
    def test_can_switch_guards(self):
        self.get('/guard/web').assertContains('False')
        self.assertIsInstance(self.container.make(Auth).get(), WebGuard)
        
        self.get('/guard/api').assertContains('user')
        self.assertIsInstance(self.container.make(Auth).get(), WebGuard)