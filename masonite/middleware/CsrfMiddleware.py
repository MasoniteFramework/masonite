"""CSRF Middleware."""

from jinja2 import Markup

from masonite.auth import Csrf
from masonite.exceptions import InvalidCSRFToken
from masonite.request import Request
from masonite.view import View


class CsrfMiddleware:
    """Verify CSRF Token Middleware."""

    exempt = ['/']
    every_request = True
    token_length = 30

    def __init__(self, request: Request, csrf: Csrf, view: View):
        """Initialize the CSRF Middleware

        Arguments:
            request {masonite.request.Request} -- The normal Masonite request class.
            csrf {masonite.auth.Csrf} -- CSRF auth class.
            view {masonite.view.View} -- The normal Masonite view class.
        """

        self.request = request
        self.csrf = csrf
        self.view = view

    def before(self):
        """Execute this method before the controller."""

        token = self.verify_token()

        self.view.share({
            'csrf_field': Markup("<input type='hidden' name='__token' value='{0}' />".format(token)),
            'csrf_token': token
        })

    def after(self):
        pass

    def in_exempt(self):
        """Determine if the request has a URI that should pass through CSRF verification.

        Returns:
            bool
        """
        for route in self.exempt:
            if self.request.contains(route):
                return True

        return False

    def generate_token(self):
        """Generate a token that will be used for CSRF protection

        Returns:
            string -- A random string based on the length given
        """

        return self.csrf.generate_csrf_token(self.token_length)

    def verify_token(self):
        """Verify if csrf token in post is valid.

        Raises:
            InvalidCSRFToken -- Thrown if the CSRF tokens do not match.

        Returns:
            string -- Returns a new token or the current token.
        """

        if self.request.is_post() and not self.in_exempt():
            token = self.request.input('__token')
            if not self.csrf.verify_csrf_token(token):
                raise InvalidCSRFToken("Invalid CSRF token.")
            return token
        else:
            if not self.every_request and self.request.get_cookie('csrf_token', decrypt=False):
                return self.request.get_cookie('csrf_token', decrypt=False)
            else:
                return self.generate_token()
