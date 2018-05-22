from masonite.app import App
from masonite.controllers import Controller


class TestController:
    
    def setup_method(self):
        self.app = App()
        self.app.bind('object', object)
    
    def test_controller_loads_app(self):
        controller = Controller().load_app(self.app)
        assert controller.app.providers == {'object': object}
