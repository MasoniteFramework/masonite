"""CSRF Protection Module."""
import binascii
import os


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
        token = bytes(binascii.b2a_hex(os.urandom(length // 2))).decode('utf-8')
        self.request.cookie('csrf_token', token, encrypt=False)
        return token

    def verify_csrf_token(self, token):
        """Verify if csrf token is valid from the cookie set.

        Arguments:
            token {string} -- The token that was generated.

        Returns:
            bool
        """
        if self.request.get_cookie('csrf_token', decrypt=False) == token:
            return True
        else:
            return False
