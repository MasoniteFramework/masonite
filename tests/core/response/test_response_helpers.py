from tests import TestCase
from src.masonite.routes import Route


class TestResponseHelpers(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test-with-errors", "WelcomeController@with_errors"),
            Route.get("/test-with-input", "WelcomeController@form_with_input"),
        )

    def test_with_input(self):
        res = self.get("/test-with-input", {"name": "Sam"}).assertSessionHas(
            "name", "Sam"
        )

    def test_with_errors(self):
        self.get("/test-with-errors").assertSessionHasErrors().assertSessionHasErrors(
            ["email"]
        )
