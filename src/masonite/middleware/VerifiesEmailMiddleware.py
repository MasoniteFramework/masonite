from .middleware import Middleware


class VerifiesEmailMiddleware(Middleware):
    def before(self, request, response):
        user = request.user()
        if not user:
            return response.redirect("/login")
        if not hasattr(user, "has_verified_email") or not user.has_verified_email():
            return response.redirect("/email/verify/notice")
        return request

    def after(self, request, response):
        return request
