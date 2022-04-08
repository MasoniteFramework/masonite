from tests import TestCase
from src.masonite.routes import Route
from src.masonite.middleware import CorsMiddleware


class TestCors(TestCase):
    def setUp(self):
        super().setUp()
        # add CorsMiddleware
        self.application.make("middleware").add([CorsMiddleware])
        self.cors = self.application.make("cors")
        self.cors.set_options(
            {
                "allowed_origins": ["http://localhost"],
                "allowed_headers": ["X-Test-1"],
                "allowed_methods": ["GET", "POST"],
                "exposed_headers": [],
                "max_age": 0,
                "support_credentials": False,
                "paths": ["api/*"],
            }
        )
        self.addRoutes(
            Route.post(
                "/api/test", "tests.integrations.controllers.api.TestController@show"
            ),
            Route.put(
                "/api/test", "tests.integrations.controllers.api.TestController@show"
            ),
            Route.get("/", "WelcomeController@test"),
            Route.post("/", "WelcomeController@api"),
        )

    def test_todo(self):
        self.withHeaders(
            {
                "Access-Control-Request-Method": "POST",
            }
        ).options("/api/test").dumpSession().dumpHeaders().assertNoContent()
