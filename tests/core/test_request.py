
from src.masonite.drivers import SessionMemoryDriver
from src.masonite.managers import SessionManager
from src.masonite.testing import generate_wsgi, TestCase

class TestSession(TestCase):

    def setUp(self):
        super().setUp()
        self.container.make('Request').load_environ(generate_wsgi())
        self.container.bind('SessionMemoryDriver', SessionMemoryDriver)
        self.container.bind('SessionManager', SessionManager(self.container))

    def test_intended_returns_correct_url(self):
        request = self.container.make('Request')
        request.intended(default='/dashboard')
        self.assertEqual(request.redirect_url, '/dashboard')

        request.with_intended('/admin')
        request.intended()
        self.assertEqual(request.redirect_url, '/admin')
