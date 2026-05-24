import inspect
import unittest
from unittest.mock import MagicMock, patch

from src.masonite.auth import Sign, MustVerifyEmail
from src.masonite.exceptions import InvalidToken
from src.masonite.middleware import VerifiesEmailMiddleware

# A stable Fernet key used only in tests so Sign() never touches wsgi
TEST_KEY = "ODgUEaNUZqBweffQP9Rw1U_KEqL2EIcgjfQIsLPnL6g="


class MockUser(MustVerifyEmail):
    """Minimal user stub that mixes in MustVerifyEmail."""

    def __init__(self, user_id=1, email="user@example.com", name="Test", verified_at=None):
        self.id = user_id
        self.email = email
        self.name = name
        self.verified_at = verified_at
        self._saved = False

    def save(self):
        self._saved = True


# ---------------------------------------------------------------------------
# MustVerifyEmail mixin
# ---------------------------------------------------------------------------

class TestMustVerifyEmailMixin(unittest.TestCase):

    def test_unverified_user_returns_false(self):
        self.assertFalse(MockUser(verified_at=None).has_verified_email())

    def test_verified_user_returns_true(self):
        self.assertTrue(MockUser(verified_at="2026-01-01 00:00:00").has_verified_email())

    def test_mark_email_as_verified_sets_timestamp(self):
        user = MockUser(verified_at=None)
        user.mark_email_as_verified()
        self.assertIsNotNone(user.verified_at)

    def test_mark_email_as_verified_calls_save(self):
        user = MockUser(verified_at=None)
        user.mark_email_as_verified()
        self.assertTrue(user._saved)

    def test_mark_email_as_verified_makes_has_verified_email_true(self):
        user = MockUser(verified_at=None)
        user.mark_email_as_verified()
        self.assertTrue(user.has_verified_email())

    def test_verify_email_sends_mail(self):
        user = MockUser()
        mail_manager = MagicMock()
        request = MagicMock()
        request.environ = {"wsgi.url_scheme": "http", "HTTP_HOST": "localhost"}

        with patch("src.masonite.auth.MustVerifyEmail.Sign", lambda: Sign(key=TEST_KEY)):
            user.verify_email(mail_manager, request)

        mail_manager.mailable.assert_called_once()
        mail_manager.mailable.return_value.send.assert_called_once()

    def test_verify_email_token_contains_user_id(self):
        """Token must unsign to a payload that starts with the user id."""
        user = MockUser(user_id=42)
        mail_manager = MagicMock()
        request = MagicMock()
        request.environ = {"wsgi.url_scheme": "http", "HTTP_HOST": "localhost"}

        with patch("src.masonite.auth.MustVerifyEmail.Sign") as MockSign:
            user.verify_email(mail_manager, request)
            raw_value = MockSign.return_value.sign.call_args[0][0]

        self.assertTrue(raw_value.startswith("42::"))

    def test_verify_email_uses_correct_recipient(self):
        user = MockUser(email="jane@example.com")
        captured = {}

        def capture(mailable):
            captured["mailable"] = mailable
            return MagicMock()

        mail_manager = MagicMock()
        mail_manager.mailable.side_effect = capture
        request = MagicMock()
        request.environ = {"wsgi.url_scheme": "http", "HTTP_HOST": "localhost"}

        with patch("src.masonite.auth.MustVerifyEmail.Sign"):
            user.verify_email(mail_manager, request)

        # Mailable stores the recipient in _to (set via .to())
        self.assertEqual(captured["mailable"]._to, "jane@example.com")


# ---------------------------------------------------------------------------
# Sign utility
# ---------------------------------------------------------------------------

class TestSign(unittest.TestCase):

    def setUp(self):
        self.sign = Sign(key=TEST_KEY)

    def test_sign_and_unsign_round_trip(self):
        original = "42::1716000000.0"
        self.assertEqual(self.sign.unsign(self.sign.sign(original)), original)

    def test_unsign_invalid_token_raises(self):
        with self.assertRaises(InvalidToken):
            self.sign.unsign("not-a-valid-token")

    def test_different_values_produce_different_tokens(self):
        self.assertNotEqual(self.sign.sign("1::1000"), self.sign.sign("2::1000"))


# ---------------------------------------------------------------------------
# VerifiesEmailMiddleware
# ---------------------------------------------------------------------------

class TestVerifiesEmailMiddleware(unittest.TestCase):

    def setUp(self):
        self.middleware = VerifiesEmailMiddleware()

    def _mock_request_response(self, user=None):
        request = MagicMock()
        request.user.return_value = user
        response = MagicMock()
        return request, response

    def test_unauthenticated_user_is_redirected_to_login(self):
        request, response = self._mock_request_response(user=None)
        self.middleware.before(request, response)
        response.redirect.assert_called_once_with("/login")

    def test_unverified_user_is_redirected_to_notice(self):
        user = MockUser(verified_at=None)
        request, response = self._mock_request_response(user=user)
        self.middleware.before(request, response)
        response.redirect.assert_called_once_with("/email/verify/notice")

    def test_verified_user_passes_through(self):
        user = MockUser(verified_at="2026-01-01 00:00:00")
        request, response = self._mock_request_response(user=user)
        result = self.middleware.before(request, response)
        response.redirect.assert_not_called()
        self.assertEqual(result, request)

    def test_user_without_mixin_is_redirected_to_notice(self):
        plain_user = object()  # no has_verified_email attribute
        request, response = self._mock_request_response(user=plain_user)
        self.middleware.before(request, response)
        response.redirect.assert_called_once_with("/email/verify/notice")

    def test_after_always_passes_through(self):
        request, response = self._mock_request_response()
        self.assertEqual(self.middleware.after(request, response), request)


# ---------------------------------------------------------------------------
# Auth.routes() includes verification routes
# Inspect source rather than calling Auth.routes() to avoid wsgi bootstrap.
# ---------------------------------------------------------------------------

class TestAuthRoutesIncludeVerification(unittest.TestCase):

    def setUp(self):
        from src.masonite.authentication import Auth
        self.source = inspect.getsource(Auth.routes)

    def test_verification_notice_route_defined(self):
        self.assertIn("verification.notice", self.source)

    def test_verification_verify_route_defined(self):
        self.assertIn("verification.verify", self.source)

    def test_verification_resend_route_defined(self):
        self.assertIn("verification.resend", self.source)

    def test_verify_route_has_token_param(self):
        self.assertIn("/email/verify/@token", self.source)

    def test_resend_route_is_post(self):
        # The resend route must use Route.post
        resend_idx = self.source.index("verification.resend")
        snippet = self.source[max(0, resend_idx - 200):resend_idx]
        self.assertIn("Route.post", snippet)


if __name__ == "__main__":
    unittest.main()
