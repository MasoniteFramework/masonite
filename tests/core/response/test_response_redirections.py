from tests import TestCase
from src.masonite.foundation import Application
import os
from src.masonite.response import Response
from src.masonite.routes import Router, Route


class TestResponseRedirect(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(Route.get("/", None).name("home-redirect"))
        self.response = Response(self.application)

    def test_redirect(self):
        self.response.redirect("/")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/")

    def test_redirect_to_route_named_route(self):
        self.response.redirect(name="home-redirect")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/")

    def test_redirect_to_url(self):
        self.response.redirect(url="/login")
        self.assertEqual(self.response.get_status(), 302)
        self.assertEqual(self.response.header_bag.get("Location").value, "/login")
