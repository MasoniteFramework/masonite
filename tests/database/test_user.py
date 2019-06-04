"""Example Database Testcase."""

from masonite.testing import DatabaseTestCase

from app.User import User


class TestUser(DatabaseTestCase):

    def setUp(self):
        """Anytime you override the setUp method you must call the setUp method
        on the parent class like below.
        """
        super().setUp()

    def setUpFactories(self):
        """This runs when the test class first starts up.
        This does not run before every test case.
        """
        self.make(User, self.users_factory)

    def users_factory(self, faker):
        """Example factory

        Arguments:
            faker {faker.Faker} -- An instance of Faker

        Returns:
            dict
        """
        return {
            'name': faker.name(),
            'email': faker.email(),
            'password': '$2b$12$WMgb5Re1NqUr.uSRfQmPQeeGWudk/8/aNbVMpD1dR.Et83vfL8WAu',  # == 'secret'
        }

    def test_created_user(self):
        self.assertTrue(User.find(1))

    def test_created_50_users(self):
        self.assertEqual(User.count(), 50)
