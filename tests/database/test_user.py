"""Example Database Testcase."""

from masonite.testing import TestCase

from app.User import User
from config.factories import factory


class TestUser(TestCase):

    def setUp(self):
        """Anytime you override the setUp method you must call the setUp method
        on the parent class like below.
        """
        super().setUp()

    def setUpFactories(self):
        """This runs when the test class first starts up.
        This does not run before every test case.
        """
        factory(User, 1).create()

    def test_created_user(self):
        self.assertTrue(User.find(1))
