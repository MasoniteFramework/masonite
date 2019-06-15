from masonite.app import App
from masonite.hook import Hook
import unittest


class SentryExceptionHookMock:
    def load(self, _):
        return 'loaded'


class TestFrameworkHooks(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('SentryExceptionHook', SentryExceptionHookMock())
        self.app.bind('HookHandler', Hook(self.app))

    def test_exception_handler(self):
        self.assertIsNone(self.app.make('HookHandler').fire('*ExceptionHook'))
