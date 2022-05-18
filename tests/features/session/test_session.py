from src.masonite.drivers.session import CookieDriver
from tests import TestCase


class TestSession(TestCase):
    def test_default_sessiondriver(self):
        session = self.application.make("session")
        session.start("cookie")
        driver = session.get_driver()
        self.assertIsInstance(driver, CookieDriver)

