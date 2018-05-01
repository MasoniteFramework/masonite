from masonite.app import App
from masonite.hook import Hook

app = App()

class SentryExceptionHook:
    def load(self, app):
        return 'loaded'

app.bind('SentryExceptionHook', SentryExceptionHook())
app.bind('HookHandler', Hook(app))

def test_exception_handler():
    assert app.make('HookHandler').fire('*ExceptionHook') is None

