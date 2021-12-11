from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth
from masonite.facades import Mail
from app.mailables.ResetPassword import ResetPassword


class PasswordResetController(Controller):
    def show(self, view: View):  # Show password_reset page
        return view.render("auth.password_reset")

    def store(self, auth: Auth, request: Request, response: Response):
        email, reset_token = auth.password_reset(request.input("email"))
        if email:
            Mail.mailable(ResetPassword(token=reset_token).to(email)).send()
        return response.back().with_success(
            [
                "Email sent. Please follow the directions in your email to complete your password reset."
            ]
        )

    def change_password(self, view: View, request: Request):
        return view.render("auth.change_password", {"token": request.param("token")})

    def store_changed_password(self, auth: Auth, request: Request, response: Response):
        errors = request.validate(
            {
                "password": "required|strong|confirmed",
            }
        )

        if errors:
            return response.back().with_errors(errors)

        if auth.reset_password(request.input("password"), request.param("token")):
            return response.back().with_success(["Password Reset Successfully"])

        return response.back().with_errors(["Could not reset your password"])
