import binascii
import os


class Csrf(object):
    """
    Class for csrf protection
    """

    def __init__(self, request):
        self.request = request

    def generate_csrf_token(self):
        """
        Generate token for csrf protection
        """

        token = binascii.b2a_hex(os.urandom(15))
        self.request.cookie('csrftoken', token)

    def verify_csrf_token(self, token):
        """
        Verify if csrf token is valid
        """

        if self.request.get_cookie('csrftoken') == token:
            return True
        else:
            return False
