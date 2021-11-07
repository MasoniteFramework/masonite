from tests import TestCase
from masoniteorm.models import Model

from src.masonite.authorization import Authorizes
from src.masonite.facades import Gate


class User(Model, Authorizes):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


class TestAuthorizes(TestCase):
    def setUp(self):
        super().setUp()
        self.make_request()

    def test_user_can(self):
        user = User.find(1)
        Gate.define("create-post", lambda user: user.email == "idmann509@gmail.com")
        self.assertTrue(user.can("create-post"))

    def test_user_cannot(self):
        user = User.find(1)
        Gate.define("delete-post", lambda user: False)
        self.assertTrue(user.cannot("delete-post"))
        Gate.define("view-admin-panel", lambda user: user.email == "admin@gmail.com")
        self.assertTrue(user.cannot("view-admin-panel"))
