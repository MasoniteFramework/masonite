from masonite.app import App
from masonite.controllers import Controller
from masonite.helpers.routes import get
from app.http.controllers.ControllerTest import ControllerTest
from masonite.request import Request


def test_controller_loads_app():
    app = App()
    app.bind('object', object)

    controller = Controller().load_app(app)
    assert controller.app.providers == {'object': object}


def test_string_controller_constructor_resolves_container():
    app = App()
    app.bind('Request', Request)

    # Create the route
    route = get('/url', 'ControllerTest@show')

    # Resolve the controller constructor
    controller = app.resolve(route.controller)

    # Resolve the method
    response = app.resolve(getattr(controller, route.controller_method))

    assert isinstance(route.controller, ControllerTest.__class__)
    assert route.controller_method == 'show'
    assert isinstance(response, Request.__class__)


def test_object_controller_constructor_resolves_container():
    app = App()
    app.bind('Request', Request)

    # Create the route
    route = get('/url', ControllerTest.show)
