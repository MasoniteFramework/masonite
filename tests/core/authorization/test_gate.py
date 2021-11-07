from tests import TestCase
from masoniteorm.models import Model

from src.masonite.exceptions.exceptions import AuthorizationException, GateDoesNotExist
from src.masonite.authorization import AuthorizationResponse
from src.masonite.routes import Route


class User(Model):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


class Post(Model):
    __fillable__ = ["user_id", "name"]


class TestGate(TestCase):
    def setUp(self):
        super().setUp()
        self.gate = self.application.make("gate")
        self.make_request()
        self.make_response()
        self.addRoutes(
            Route.get("/not-authorized", "WelcomeController@not_authorized"),
            Route.get(
                "/authorize-helper", "WelcomeController@use_authorization_helper"
            ),
            Route.get("/authorizations", "WelcomeController@authorizations"),
        )

    def tearDown(self):
        super().tearDown()
        self.gate.permissions = {}
        self.gate.before_callbacks = []
        self.gate.after_callbacks = []

    def test_can_define_gates(self):
        self.gate.define(
            "create-post", lambda user: user.email == "idmann509@gmail.com"
        )
        self.gate.define("view-post", lambda user: True)
        self.assertEqual(
            list(self.gate.permissions.keys()), ["create-post", "view-post"]
        )

    def test_can_use_for_user(self):
        given_user = User()
        user = self.gate.for_user(given_user)._get_user()
        self.assertEqual(user, given_user)

    def test_gate_user_the_current_authenticated_request_user(self):
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        user = self.gate._get_user()
        self.assertEqual(user.email, "idmann509@gmail.com")

    def test_can_use_gate_facade(self):
        from src.masonite.facades import Gate

        self.assertEqual(self.gate.define, Gate.define)

    def test_denies_guests_users(self):
        self.gate.define("create-post", lambda user: True)
        # above permission should always been allowed but user is not authenticated
        self.assertTrue(self.gate.denies("create-post"))

    def test_allows_guests_users_if_specified(self):
        # it can be specified by allowing user to be optional
        self.gate.define("create-post", lambda user=None: True)
        # above permission should always been allowed even for guests users
        self.assertTrue(self.gate.allows("create-post"))

    def test_allows_and_denies(self):
        self.gate.define(
            "create-post", lambda user: user.email == "idmann509@gmail.com"
        )
        self.gate.define("view-post", lambda user: False)
        # authenticate user
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")

        self.assertTrue(self.gate.allows("create-post"))
        self.assertFalse(self.gate.denies("create-post"))
        self.assertFalse(self.gate.allows("view-post"))
        self.assertTrue(self.gate.denies("view-post"))

    def test_allows_with_arg(self):
        self.gate.define("update-post", lambda user, post: post.user_id == user.id)
        # authenticate user
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        # create a post for the user 1
        post = Post()
        post.user_id = 1
        post2 = Post()
        post2.user_id = 3
        self.assertTrue(self.gate.allows("update-post", post))
        self.assertFalse(self.gate.allows("update-post", post2))

    def test_gate_has_permission(self):
        self.gate.define("display-admin", lambda user: False)
        self.assertTrue(self.gate.has("display-admin"))
        self.assertFalse(self.gate.has("view-user"))

    def test_authorize(self):
        self.gate.define("display-admin", lambda user: False)
        with self.assertRaises(AuthorizationException) as e:
            self.gate.authorize("display-admin")
            exception = e.exception
        self.assertEqual(e.exception.message, "Action not authorized")
        self.assertEqual(e.exception.status, 403)

    def test_authorize_in_controller(self):
        self.withExceptionsHandling()  # this will allow exception to be handled and rendered
        self.gate.define("display-admin", lambda user: False)
        self.get("/not-authorized").assertForbidden().assertContains(
            "Action not authorized"
        )

    def test_inspect(self):
        self.gate.define("display-admin", lambda user: False)
        response = self.gate.inspect("display-admin")
        self.assertIsInstance(response, AuthorizationResponse)
        self.assertFalse(response.allowed())

    def test_define_gate_returning_response(self):
        self.gate.define(
            "display-admin",
            lambda user: AuthorizationResponse.allow()
            if user.email == "admin@masonite.com"
            else AuthorizationResponse.deny("You shall not pass"),
        )
        # authenticate user
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        response = self.gate.inspect("display-admin")
        self.assertFalse(response.allowed())
        self.assertEqual(response.message(), "You shall not pass")

    def test_gate_before(self):
        self.gate.before(lambda user, permission: user.email == "idmann509@gmail.com")
        # a permission that is always False
        self.gate.define("display-admin", lambda user: False)
        # authenticate user
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        self.assertTrue(self.gate.allows("display-admin"))

    def test_gate_after(self):
        self.gate.after(lambda user, permission, result: False)
        # a permission that is always False
        self.gate.define("display-admin", lambda user: True)
        # authenticate user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        self.assertTrue(self.gate.denies("display-admin"))

    def test_any(self):
        self.gate.define("delete-post", lambda user, post: True)
        self.gate.define("update-post", lambda user, post: user.id == post.user_id)
        # authenticate user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        post = Post()
        post.user_id = 1
        self.assertTrue(self.gate.any(["update-post", "delete-post"], post))

    def test_none(self):
        self.gate.define("force-delete-post", lambda user, post: False)
        self.gate.define(
            "restore-post", lambda user, post: user.email == "admin@gmail.com"
        )
        # authenticate user 1
        self.application.make("auth").attempt("idmann509@gmail.com", "secret")
        post = Post()
        self.assertTrue(self.gate.none(["force-delete-post", "restore-post"], post))

    def test_unknown_gate_raises_exception(self):
        with self.assertRaises(GateDoesNotExist):
            self.gate.allows("can-fly")

    def test_view_helpers(self):
        self.gate.define("view-posts", lambda user=None: True)
        self.gate.define(
            "display-admin", lambda user: user.email == "idmann509@gmail.com"
        )
        self.get("/authorizations").assertContains(
            "User can view posts"
        ).assertContains("User cannot display admin")

    # def test_can_use_authorize_helper_on_request(self):
    #     self.gate.define("display-admin", lambda user: True)
    #     # authenticate user : here it does not work => no user in request inside Gate...
    #     # something is going on
    #     self.application.make("auth").attempt("idmann509@gmail.com", "secret")
    #     self.get("/authorize-helper").assertOk()
