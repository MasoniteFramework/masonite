from tests import TestCase
from src.masonite.routes import Route
from src.masonite.middleware import CorsMiddleware


class TestCors(TestCase):
    def setUp(self):
        super().setUp()
        # add CorsMiddleware
        self.application.make("middleware").add([CorsMiddleware])
        self.cors = self.application.make("cors")
        self.default_options = {
            "allowed_origins": ["http://localhost"],
            "allowed_headers": ["X-Test-1", "X-Test-2"],
            "allowed_methods": ["GET", "POST"],
            "exposed_headers": [],
            "max_age": 0,
            "support_credentials": False,
            "paths": ["api/*"],
        }
        self.cors.set_options(self.default_options)
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

    def tearDown(self):
        super().tearDown()
        # reset CORS options to test default
        self.cors.set_options(self.default_options)

    def test_response_when_origin_not_allowed(self):
        self.withHeaders(
            {
                "Origin": "http://djangoproject.com",
                "Access-Control-Request-Method": "POST",
            }
        ).options("/api/test").assertNoContent().assertHasHeader(
            "Access-Control-Allow-Origin", "http://localhost"
        )

    def test_access_control_allow_origin_if_no_origin(self):
        self.withHeaders({"Access-Control-Request-Method": "POST",}).options(
            "/api/test"
        ).assertNoContent().assertHasHeader(
            "Access-Control-Allow-Origin", "http://localhost"
        )

    def test_access_control_allow_origin_if_origin(self):
        self.withHeaders(
            {
                "Origin": "http://localhost",
                "Access-Control-Request-Method": "POST",
            }
        ).options("/api/test").assertNoContent().assertHasHeader(
            "Access-Control-Allow-Origin", "http://localhost"
        )

    def test_allow_all_origins(self):
        self.cors.set_options({**self.default_options, "allowed_origins": ["*"]})

        self.withHeaders(
            {
                "Origin": "https://masoniteproject.com",
                "Access-Control-Request-Method": "POST",
            }
        ).options("/api/test").assertNoContent().assertHasHeader(
            "Access-Control-Allow-Origin", "*"
        )

    def test_response_when_method_allowed(self):
        self.withHeaders(
            {
                "Origin": "http://localhost",
                "Access-Control-Request-Method": "POST",
            }
        ).post("/api/test").assertOk().assertContains(
            "welcome"
        ).dumpResponseHeaders().assertHeaderMissing(
            "Access-Control-Allow-Methods"
        )

    def test_response_when_method_not_allowed(self):
        self.withHeaders(
            {
                "Origin": "http://localhost",
                "Access-Control-Request-Method": "PUT",
            }
        ).post("/api/test").assertOk().assertHeaderMissing(
            "Access-Control-Allow-Methods"
        )

    def test_allow_headers(self):
        self.withHeaders(
            {
                "Origin": "https://masoniteproject.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "x-test-1, x-test-2",
            }
        ).options("/api/test").assertNoContent().assertHasHeader(
            "Access-Control-Allow-Headers", "x-test-1, x-test-2"
        )

    def test_allow_headers_when_header_not_allowed(self):
        self.withHeaders(
            {
                "Origin": "https://masoniteproject.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "x-other-3",
            }
        ).options("/api/test").assertNoContent().assertHasHeader(
            "Access-Control-Allow-Headers", "x-test-1, x-test-2"
        )

    def test_response_with_allowed_header(self):
        self.withHeaders(
            {
                "Origin": "http://localhost",
                "Access-Control-Request-Headers": "X-Test-1",
            }
        ).post("/api/test").assertOk().assertContains("welcome").assertHeaderMissing(
            "Access-Control-Allow-Headers"
        )

    def test_allow_all_origins_with_wildcard(self):
        self.cors.set_options(
            {**self.default_options, "allowed_origins": ["*.masoniteproject.com"]}
        )

        self.withHeaders(
            {
                "Origin": "https://docs.masoniteproject.com",
                "Access-Control-Request-Method": "POST",
            }
        ).options("/api/test").assertNoContent().dumpResponseHeaders().assertHasHeader(
            "Access-Control-Allow-Origin", "*.masoniteproject.com"
        )
