""" CSRF Protection Module """
import binascii
import os


class Csrf:
    """CSRF Protection Class
    """

    def __init__(self, request):
        """CSRF constructor

        Arguments:
            request {masonite.request.Request} -- Request object
        """

        self.request = request

    def generate_csrf_token(self):
        """Generate CRSRF token

        Returns:
            string -- Returns token generated
        """

        token = bytes(binascii.b2a_hex(os.urandom(15))).decode('utf-8')
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
