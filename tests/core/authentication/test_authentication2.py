from tests import TestCase


class TestAuthentication(TestCase):
    def setUp(self):
        super().setUp()
        self.auth = self.application.make("auth")
        self.make_request()
        self.make_response()

    def test_attempt(self):
        self.assertTrue(self.auth.attempt("idmann509@gmail.com", "secret"))
        self.assertFalse(self.auth.attempt("idmann509@gmail.com", "secret1"))

    def test_auth_class_registers_cookie(self):
        self.auth.guard("web").attempt("idmann509@gmail.com", "secret")
        self.assertTrue(self.application.make("response").cookie("token"))

    def test_logout(self):
        self.application.make("auth").guard("web").attempt(
            "idmann509@gmail.com", "secret"
        )

        self.assertTrue(self.application.make("response").cookie("token"))

        self.application.make("auth").guard("web").logout()
        self.assertTrue(
            self.application.make("response").cookie_jar.deleted_cookies["token"]
        )

    def test_attempt_by_id(self):
        self.application.make("auth").guard("web").attempt_by_id(1)

        self.assertTrue(self.application.make("response").cookie("token"))

        self.application.make("auth").guard("web").logout()
        self.assertFalse(self.application.make("response").cookie("token"))

    def test_attempt_by_id_once(self):
        self.application.make("auth").guard("web").attempt_by_id(1, once=True)

        self.assertIsNone(self.application.make("request").cookie("token"))
