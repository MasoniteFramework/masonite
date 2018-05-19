from masonite.app import App
from masonite.view import View
from masonite.exception_handler import ExceptionHandler
from masonite.hook import Hook
import pytest
from masonite.exceptions import MissingContainerBindingNotFound

class ApplicationMock:
    DEBUG = True

class StorageMock:
    STATICFILES = {}


class TestException:

    def setup_method(self):
        self.app = App()
        self.app.bind('Application', ApplicationMock)
        self.app.bind('View', View(self.app).render)
        self.app.bind('Storage', StorageMock)
        self.app.bind('ExceptionHandler', ExceptionHandler(self.app))
        self.app.bind('HookHandler', Hook(self.app))

    def test_exception_renders_view(self):
        with pytest.raises(MissingContainerBindingNotFound):
            assert self.app.make('ExceptionHandler').load_exception(KeyError)

    def test_exception_raises_exception(self):
        self.app.make('Application').DEBUG = False
        with pytest.raises(KeyError):
            assert self.app.make('ExceptionHandler').load_exception(KeyError)
