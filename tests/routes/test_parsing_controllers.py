from unittest import TestCase

from src.masonite.routes import Route
from tests.integrations.controllers.WelcomeController import WelcomeController


class SomeController:
    def method(self):
        return "hello from method"

    def __call__(self):
        return "hello"


class TestParsingControllerInRoutes(TestCase):
    def setUp(self):
        Route.set_controller_locations("tests.integrations.controllers")
        pass

    def test_use_controller_string_with_method(self):
        route = Route.get("/home", "WelcomeController@test")
        assert route.controller_class == WelcomeController
        assert route.controller_method == "test"
        assert route.get_response() == "test"

    def test_use_controller_string_without_method(self):
        route = Route.get("/home", "WelcomeController")
        assert route.controller_class == WelcomeController
        assert route.controller_method == "__call__"
        assert route.get_response() == "welcome"

    def test_use_controller_class_with_method(self):
        route = Route.get("/home", WelcomeController.test)
        assert route.controller_class == WelcomeController
        assert route.controller_method == "test"
        assert route.get_response() == "test"

    def test_use_controller_class_without_method(self):
        route = Route.get("/home", SomeController)
        assert route.controller_class == SomeController
        assert route.controller_method == "__call__"
        assert route.get_response() == "hello"

    def test_use_controller_instance_without_method(self):
        controller = SomeController()
        route = Route.get("/home", controller)
        assert route.controller_instance == controller
        assert route.controller_method == "__call__"
        assert route.get_response() == "hello"

    def test_use_controller_instance_with_method(self):
        controller = SomeController()
        route = Route.get("/home", controller.method)
        assert route.controller_instance == controller
        assert route.controller_method == "method"
        assert route.get_response() == "hello from method"
