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

container = App()
container.bind('Application', ApplicationMock)
container.bind('View', View(container).render)
container.bind('Storage', StorageMock)
container.bind('ExceptionHandler', ExceptionHandler(container))
container.bind('HookHandler', Hook(app))

def test_exception_renders_view():
    with pytest.raises(MissingContainerBindingNotFound):
        assert container.make('ExceptionHandler').load_exception(KeyError)


def test_exception_raises_exception():
    container.make('Application').DEBUG = False
    with pytest.raises(KeyError):
        assert container.make('ExceptionHandler').load_exception(KeyError)
