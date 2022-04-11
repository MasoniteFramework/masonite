from tests import TestCase
from src.masonite.response import Response
from src.masonite.routes import Route


class TestResponseRedirect(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(Route.get("/", None).name("home-redirect"))
        self.response = Response(self.application)

    def test_redirect(self):
        self.response.redirect("/")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/")

        self.response.redirect("/", query_params={"key": "value"})
        self.assertEqual(self.response.header_bag.get("Location").value, "/?key=value")

    def test_redirect_to_route_named_route(self):
        self.response.redirect(name="home-redirect")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/")

        self.response.redirect(name="home-redirect", query_params={"key": "value"})
        self.assertEqual(self.response.header_bag.get("Location").value, "/?key=value")

    def test_redirect_to_url(self):
        self.response.redirect(url="/login")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/login")

        self.response.redirect(url="/login", query_params={"key": "value"})
        self.assertEqual(
            self.response.header_bag.get("Location").value, "/login?key=value"
        )
