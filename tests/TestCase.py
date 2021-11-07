from src.masonite.tests import TestCase
from src.masonite.routes import Route


class TestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/", "WelcomeController@show"),
            Route.post("/", "WelcomeController@show"),
        )
