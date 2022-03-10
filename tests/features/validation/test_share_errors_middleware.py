from tests import TestCase
from src.masonite.routes import Route


class TestShareErrorsMiddleware(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/contact-us,", "WelcomeController@contact"),
            Route.post("/contact", "WelcomeController@contact_post"),
        )

    def test_validation_errors_are_shared(self):
        response = self.post("/contact", {"name": "Sam"})

        response.assertRedirect()

        errors = self.application.make("view")._shared.get("errors")
        import pdb

        pdb.set_trace()
