from src.masonite.middleware import SessionMiddleware
from src.masonite.routes import Route
from tests import TestCase


class TestResponseHelpers(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/test-with-errors", "WelcomeController@with_errors"),
            Route.get("/test-with-input", "WelcomeController@form_with_input"),
        )

    def test_with_input(self):
        self.get("/test-with-input", {"name": "Sam"}).assertSessionHas("name", "Sam")

    def test_with_errors(self):
        self.get("/test-with-errors").assertSessionHasErrors().assertSessionHasErrors(
            ["email"]
        )


class TestResponseWithMiddleware(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("middleware").add(
            {
                "web": SessionMiddleware,
            }
        )
        self.addRoutes(
            Route.get("/test-with-errors", "WelcomeController@with_errors").middleware(
                "web"
            ),
            Route.get(
                "/test-with-input", "WelcomeController@form_with_input"
            ).middleware("web"),
        )

    def test_with_input(self):
        (
            self.get("/test-with-input", {"name": "Sam"})
            .assertSessionHas("name", "Sam")
            .assertSessionHasNoErrors()
        )

    def test_with_errors(self):
        (
            self.get("/test-with-errors")
            .assertSessionHasErrors()
            .assertSessionHasErrors(["email"])
            .assertSessionHasNoErrors()
        )
