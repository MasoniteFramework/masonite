"""CSRF Protection Module."""
import binascii
import os
from hmac import compare_digest
from .Sign import Sign
from ..exceptions import InvalidCSRFToken
from cryptography.fernet import InvalidToken


class Csrf:
    """CSRF Protection Class."""

    def __init__(self, request):
        """CSRF constructor.

        Arguments:
            request {masonite.request.Request} -- Request object
        """
        self.request = request

    def generate_csrf_token(self, length=30):
        """Generate CRSRF token.

        The // you see below is integer division. Since the token will be twice
        the size of the length passed to. A length of 30 passed below will generate
        a string length of 60 so we integer divide by 2

        Returns:
            string -- Returns token generated.
        """
        token = self.request.get_cookie("SESSID")
        self.request.cookie("csrf_token", token)
        return token

    def verify_csrf_token(self, token):
        """Verify if csrf token is valid from the cookie set.

        Arguments:
            token {string} -- The token that was generated.

        Returns:
            bool
        """
        try:
            token = Sign().unsign(token)
        except (InvalidToken, TypeError):
            pass

        try:
            csrf_token = Sign().unsign(self.request.get_cookie("csrf_token", decrypt=False))
        except (InvalidToken, TypeError):
            csrf_token = False

        if csrf_token and compare_digest(
            csrf_token, token
        ):
            return True
        else:
            return False
