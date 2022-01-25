from .. import Middleware


class AuthenticationMiddleware(Middleware):
    """Middleware to check if the user is logged in."""

    def before(self, request, response):
        if not request.user():
            return response.redirect(name="login")
        return request

    def after(self, request, response):
        return request
