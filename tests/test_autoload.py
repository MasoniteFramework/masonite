from masonite.autoload import Autoload
from masonite.app import App
from masonite.request import Request
import pytest
from masonite.exceptions import InvalidAutoloadPath, AutoloadContainerOverwrite


class TestAutoload:

    def setup_method(self):
        self.app = App()

    def test_autoload_loads_from_directories(self):
        Autoload(self.app).load(['app/http/controllers'])
        assert self.app.make('TestController')
    
    def test_autoload_loads_from_directories_with_trailing_slash_raises_exception(self):
        with pytest.raises(InvalidAutoloadPath):
            Autoload(self.app).load(['app/http/controllers/'])
    
    def test_autoload_loads_from_directories_and_instances(self):
        classes = Autoload().instances(['app/http/controllers'], object).classes
        assert 'TestController' in classes
    
    
    def test_autoload_throws_exception_when_binding_key_that_already_exists(self):
        self.app.bind('Request', Request(None))
        with pytest.raises(AutoloadContainerOverwrite):
            Autoload(self.app).load(['app/http/test_controllers'])
