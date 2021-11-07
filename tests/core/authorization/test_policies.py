from tests import TestCase
from masoniteorm.models import Model

from tests.integrations.policies.PostPolicy import PostPolicy
from src.masonite.exceptions.exceptions import PolicyDoesNotExist


class User(Model):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


class Post(Model):
    __fillable__ = ["user_id", "name"]


class TestPolicies(TestCase):
    def setUp(self):
        super().setUp()
        self.gate = self.application.make("gate")
        self.make_request()

    def tearDown(self):
        super().tearDown()
        self.gate.policies = {}
        self.gate.permissions = {}

    def test_can_register_policies(self):
        self.gate.register_policies([(Post, PostPolicy)])
        self.assertEqual(self.gate.policies[Post], PostPolicy)

    def test_using_policies_with_argument(self):
        self.gate.register_policies([(Post, PostPolicy)])
        post = Post()
        post.user_id = 1
        # authenticates user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        self.assertTrue(self.gate.allows("update", post))

    def test_using_policies_without_argument(self):
        self.gate.register_policies([(Post, PostPolicy)])
        # authenticates user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")

        self.assertTrue(self.gate.allows("create", Post))

    def test_using_policy_returning_response(self):
        self.gate.register_policies([(Post, PostPolicy)])
        # authenticates user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        post = Post()
        post.user_id = 3
        response = self.gate.inspect("delete", post)
        self.assertFalse(response.allowed())
        self.assertEqual(response.message(), "You do not own this post")

    def test_that_use_defined_gate_if_no_policy_match(self):
        self.gate.define("update", lambda user, post: user.id == post.user_id)
        post = Post()
        post.user_id = 1
        # authenticates user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        # here no policy has been defined, the gate defined above will be used
        self.assertTrue(self.gate.allows("update", post))

    def test_that_policy_can_allow_guest_users(self):
        self.gate.register_policies([(Post, PostPolicy)])
        self.assertTrue(self.gate.allows("view_any", Post))

    def test_any_on_policy(self):
        self.gate.register_policies([(Post, PostPolicy)])
        post = Post()
        post.user_id = 1
        # authenticates user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        self.assertTrue(self.gate.any(["update", "delete"], post))

    def test_unknown_policy_method_raises_exception(self):
        self.gate.register_policies([(Post, PostPolicy)])
        with self.assertRaises(PolicyDoesNotExist):
            self.gate.allows("can-fly", Post)
