from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth
from masonite.auth import Sign
from masonite.exceptions import InvalidToken
from masonite.facades import Mail


class VerifyEmailController(Controller):
    def verify(self, request: Request, response: Response, auth: Auth):
        token = request.param("token")
        sign = Sign()

        try:
            payload = sign.unsign(token)
        except InvalidToken:
            return response.redirect("/email/verify/notice").with_errors(
                ["Invalid or expired verification link."]
            )

        user_id = payload.split("::")[0]
        user = auth.attempt_by_id(user_id, once=True)

        if not user:
            return response.redirect("/login")

        if user.has_verified_email():
            return response.redirect("/home")

        user.mark_email_as_verified()
        request.app().make("event").fire("auth.email_verified", user)

        return response.redirect("/home").with_success(
            ["Your email has been verified."]
        )

    def notice(self, request: Request, response: Response, auth: Auth):
        if auth.user() and auth.user().has_verified_email():
            return response.redirect("/home")
        return response.view("auth.verify_email_notice")

    def resend(self, request: Request, response: Response, auth: Auth):
        user = auth.user()

        if not user:
            return response.redirect("/login")

        if user.has_verified_email():
            return response.redirect("/home")

        user.verify_email(Mail, request)

        return response.back().with_success(
            ["A fresh verification link has been sent to your email address."]
        )
