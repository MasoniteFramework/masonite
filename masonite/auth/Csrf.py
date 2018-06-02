import binascii
import os


class Csrf:
    """
    Class for csrf protection
    """

    def __init__(self, request):
        self.request = request

    def generate_csrf_token(self):
        """
        Generate token for csrf protection
        """

        token = bytes(binascii.b2a_hex(os.urandom(15))).decode('utf-8')
        self.request.cookie('csrf_token', token, encrypt=False)
        return token

    def verify_csrf_token(self, token):
        """
        Verify if csrf token is valid
        """

        if self.request.get_cookie('csrf_token', decrypt=False) == token:
            return True
        else:
            return False
