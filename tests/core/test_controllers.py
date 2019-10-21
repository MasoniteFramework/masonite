from src.masonite.app import App
from src.masonite.helpers.routes import get
from app.http.controllers.ControllerTest import ControllerTest
from src.masonite.request import Request
import unittest


class TestController(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('object', object)

    def test_string_controller_constructor_resolves_container(self):
        self.app.bind('Request', Request)

        # Create the route
        route = get('/url', 'ControllerTest@show')

        # Resolve the controller constructor
        controller = self.app.resolve(route.controller)

        # Resolve the method
        response = self.app.resolve(getattr(controller, route.controller_method))

        self.assertIsInstance(route.controller, ControllerTest.__class__)
        self.assertEqual(route.controller_method, 'show')
        self.assertIsInstance(response, Request)

    def test_object_controller_constructor_resolves_container(self):
        self.app.bind('Request', Request)
        # Create the route
        route = get('/url', ControllerTest.show)

        # Resolve the controller constructor
        controller = self.app.resolve(route.controller)

        # Resolve the method
        response = self.app.resolve(
            getattr(controller, route.controller_method))

        self.assertIsInstance(route.controller, ControllerTest.__class__)
        self.assertEqual(route.controller_method, 'show')
        self.assertIsInstance(response, Request)
