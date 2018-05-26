from masonite.autoload import Autoload
from masonite.app import App
import pytest
from masonite.exceptions import InvalidAutoloadPath


class TestAutoload:

    def setup_method(self):
        self.app = App()

    def test_autoload_loads_from_directories(self):
        Autoload(self.app).load(['app/http/controllers'])
        assert self.app.make('TestController')
    
    def test_autoload_loads_from_directories_with_trailing_slash_raises_exception(self):
        with pytest.raises(InvalidAutoloadPath):
            Autoload(self.app).load(['app/http/controllers/'])
    
