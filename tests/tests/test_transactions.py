from tests import TestCase
from tests.integrations.app.User import User
from src.masonite.tests import DatabaseTransactions


class TestDatabase(TestCase, DatabaseTransactions):

    connection = None

    def setUp(self):
        super().setUp()

    def test_can_use_transactions(self):
        User.create({"name": "john", "email": "john6", "password": "secret"})

    # def test_assert_deleted(self):
    #     user = User.find(1)
    #     user.delete()
    #     self.assertDeleted(user)
