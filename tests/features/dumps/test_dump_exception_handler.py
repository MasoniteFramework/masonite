from tests import TestCase

from src.masonite.routes import Route
from src.masonite.facades import Dump


class TestDumpExceptionHandler(TestCase):
    def setUp(self):
        super().setUp()
        self.addRoutes(
            Route.get("/dd", "WelcomeController@dd"),
        )

    def test_dd_display_correct_view(self):
        self.withExceptionsHandling()
        self.get("/dd").assertOk().assertViewHas("dumps").assertContains(
            "dump and die : 2 dumps"
        ).assertContains("request").assertContains("test")
        Dump.clear()
