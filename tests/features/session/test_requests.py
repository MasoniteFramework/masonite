from tests import TestCase
from src.masonite.middleware import Middleware
from src.masonite.routes import Route


class TestUpdateMiddleware(Middleware):
    def before(self, request, response):
        request.session.set("key", "value")
        request.session.flash("flash_key", "flash_value")
        return request

    def after(self, request, response):
        return request


class TestUpdateAndRedirectsMiddleware(Middleware):
    def before(self, request, response):
        request.session.set("key", "value")
        return (
            response.redirect("/home")
            .with_success("Success message")
            .with_errors("Error message")
        )

    def after(self, request, response):
        return request


class TestUpdatingSessionFromMiddlewares(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("middleware").add(
            {
                "test": TestUpdateMiddleware,
                "test_redirect": TestUpdateAndRedirectsMiddleware,
            }
        )
        self.setRoutes(
            Route.get("/", "WelcomeController@test").middleware("test"),
            Route.get("/redirect", "WelcomeController@test").middleware(
                "test_redirect"
            ),
            Route.get("/home", "WelcomeController@test"),
        )

    def test_updating_session_in_middleware_before(self):
        self.get("/").assertOk().assertSessionHas("key", "value").assertSessionHas(
            "flash_key", "flash_value"
        )

    def test_updating_session_and_redirects_in_middleware_before(self):
        response = (
            self.get("/redirect")
            .assertRedirect("/home")
            .assertSessionHas("key", "value")
            .response
        )
        # here when loading /home redirected route cookies needs to be set by the previous
        # response.
        assert response.cookie_jar.exists("f_success")
        assert response.cookie_jar.exists("f_errors")
        assert response.cookie_jar.exists("s_key")
