from masonite.testing import TestCase
from masonite.request import Request
from masonite.listeners import BaseExceptionListener
from routes.web import ROUTES
class ExceptionListener(BaseExceptionListener):

    listens = [
        ZeroDivisionError
    ]

    def __init__(self, request: Request):
        self.request = request

    def handle(self, exception, file, line):
        self.request.error_thrown = True

class ExceptionAllListener(BaseExceptionListener):

    listens = ['*']

    def __init__(self, request: Request):
        self.request = request

    def handle(self, exception, file, line):
        self.request.error_thrown = True


class TestExceptionListener(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(ROUTES)
        self.container.simple(ExceptionListener)

    def test_listener_fires(self):
        self.withExceptionHandling()
        self.assertEqual(self.get('/bad').request.error_thrown, True)

    def test_listener_doesnt_fire(self):
        self.withExceptionHandling()
        with self.assertRaises(AttributeError):
            self.assertEqual(self.get('/keyerror').request.error_thrown, True)

    def test_listener_fires_for_all(self):
        self.withExceptionHandling()
        self.container.simple(ExceptionAllListener)
        self.assertEqual(self.get('/keyerror').request.error_thrown, True)
