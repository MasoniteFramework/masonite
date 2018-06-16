from masonite.autoload import Autoload
from masonite.app import App
from masonite.request import Request
import pytest
from masonite.exceptions import InvalidAutoloadPath, AutoloadContainerOverwrite, ContainerError


class TestAutoload:

    def setup_method(self):
        self.app = App()

    def test_autoload_loads_from_directories(self):
        Autoload(self.app).load(['app/http/controllers'])
        assert self.app.make('TestController')

    def test_autoload_instantiates_classes(self):
        classes = Autoload().collect(['app/http/test_controllers'], instantiate=True)
        assert classes['TestController'].test == True  

    def test_autoload_loads_from_directories_with_trailing_slash_raises_exception(self):
        with pytest.raises(InvalidAutoloadPath):
            Autoload(self.app).load(['app/http/controllers/'])
    
    def test_autoload_raises_exception_with_no_container(self):
        with pytest.raises(ContainerError):
            Autoload().load(['app/http/controllers/'])
    
    def test_autoload_collects_classes(self):
        classes = Autoload().collect(['app/http/controllers'])
        assert 'TestController' in classes
        assert 'Command' not in classes

    def test_autoload_loads_from_directories_and_instances(self):
        classes = Autoload().instances(['app/http/controllers'], object)
        assert 'TestController' in classes
        assert 'Command' not in classes
    
    def test_autoload_loads_not_only_from_app_from_directories_and_instances(self):
        classes = Autoload().instances(['app/http/controllers'], object, only_app=False)
        assert 'TestController' in classes
        assert 'Command' in classes
    


    def test_autoload_does_not_instantiate_classes(self):
        classes = Autoload().instances(['app/http/controllers'], object)
        with pytest.raises(AttributeError):
            assert classes['TestController'].test == True
    
    def test_collects_classes_only_in_app(self):
        classes = Autoload().collect(['app/http/controllers'], only_app=False)
        assert 'TestController' in classes
        assert 'Command' in classes

    def test_autoload_throws_exception_when_binding_key_that_already_exists(self):
        self.app.bind('Request', Request(None))
        with pytest.raises(AutoloadContainerOverwrite):
            Autoload(self.app).load(['app/http/test_controllers'])
