from masonite.app import App
from masonite.controllers import Controller
from masonite.helpers.routes import get
from app.http.controllers.ControllerTest import ControllerTest
from masonite.request import Request


class TestController:

    def setup_method(self):
        self.app = App()
        self.app.bind('object', object)

    def test_controller_loads_app(self):
        controller = Controller().load_app(self.app)
        assert controller.app.providers == {'object': object}

    def test_controller_loads_app(self):
        app = App()
        app.bind('object', object)

        controller = Controller().load_app(app)
        assert controller.app.providers == {'object': object}

    def test_string_controller_constructor_resolves_container(self):
        self.app.bind('Request', Request)

        # Create the route
        route = get('/url', 'ControllerTest@show')

        # Resolve the controller constructor
        controller = self.app.resolve(route.controller)

        # Resolve the method
        response = self.app.resolve(getattr(controller, route.controller_method))

        assert isinstance(route.controller, ControllerTest.__class__)
        assert route.controller_method == 'show'
        assert isinstance(response, Request.__class__)

    def test_object_controller_constructor_resolves_container(self):
        self.app.bind('Request', Request)
        # Create the route
        route = get('/url', ControllerTest.show)

        # Resolve the controller constructor
        controller = self.app.resolve(route.controller)

        # Resolve the method
        response = self.app.resolve(
            getattr(controller, route.controller_method))

        assert isinstance(route.controller, ControllerTest.__class__)
        assert route.controller_method == 'show'
        assert isinstance(response, Request.__class__)
