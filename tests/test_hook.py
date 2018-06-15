from masonite.app import App
from masonite.hook import Hook


class SentryExceptionHookMock:
    def load(self, app):
        return 'loaded'

class TestFrameworkHooks:

    def setup_method(self):
        self.app = App()
        self.app.bind('SentryExceptionHook', SentryExceptionHookMock())
        self.app.bind('HookHandler', Hook(self.app))

    def test_exception_handler(self):
        assert self.app.make('HookHandler').fire('*ExceptionHook') is None

