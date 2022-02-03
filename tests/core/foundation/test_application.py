from tests import TestCase
from src.masonite.facades import Config


class TestApplication(TestCase):
    def test_is_running_tests(self):
        self.assertTrue(self.application.is_running_tests())

    def test_is_debug(self):
        original_value = Config.get("application.debug")

        Config.set("application.debug", True)
        self.assertTrue(self.application.is_debug())
        Config.set("application.debug", False)
        self.assertFalse(self.application.is_debug())

        Config.set("application.debug", original_value)

    def test_is_production(self):
        with self.env("production"):
            self.assertTrue(self.application.is_production())
