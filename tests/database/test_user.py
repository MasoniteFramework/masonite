"""Example Database Testcase."""

from masonite.testing import TestCase

from app.User import User
from config.factories import factory


class TestUser(TestCase):
    """Test class for User."""

    def setUp(self):
        """Call parent's setUp method.

        Anytime you override the setUp method you must call the setUp method
        on the parent class like below.
        """
        super().setUp()

    def setUpFactories(self):
        """Run when the test class first starts up.

        This does not run before every test case.
        """
        factory(User, 1).create()

    def test_created_user(self):
        """Check that we find a User."""
        self.assertTrue(User.find(1))
