from .. import Middleware
from markupsafe import Markup
from ...exceptions import InvalidCSRFToken
from hmac import compare_digest


class VerifyCsrfToken(Middleware):

    exempt = []

    def before(self, request, response):
        self.verify_token(request, self.get_token(request))

        token = self.create_token(request, response)

        request.app.make("view").share(
            {
                "csrf_field": Markup(
                    f"<input type='hidden' name='__token' value='{token}' />"
                ),
                "csrf_token": token,
            }
        )

        return request

    def after(self, request, response):
        return request

    def create_token(self, request, response):
        session = request.cookie("SESSID")
        response.cookie("csrf_token", session)
        return session

    def verify_token(self, request, token):
        if self.in_exempt(request):
            return True
        if request.is_not_safe() and not token:
            raise InvalidCSRFToken("Missing CSRF Token")
        if request.is_not_safe():
            if request.cookie("csrf_token") and (
                compare_digest(
                    request.cookie("csrf_token"),
                    token,
                )
                and compare_digest(token, request.cookie("SESSID"))
            ):
                return True
            raise InvalidCSRFToken("Invalid CSRF token.")
        return True

    def in_exempt(self, request):
        """Determine if the request has a URI that should pass through CSRF verification.

        Returns:
            bool
        """
        for route in self.exempt:
            if request.contains(route):
                return True

        return False

    def get_token(self, request):
        return (
            request.header("X-CSRF-TOKEN")
            or request.header("X-XSRF-TOKEN")
            or request.input("__token")
        )
