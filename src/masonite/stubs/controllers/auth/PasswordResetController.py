from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth


class PasswordResetController(Controller):
    def show(self, view: View):  # Show password_reset page
        return view.render("auth.password_reset")

    def store(
        self, auth: Auth, request: Request, response: Response
    ):  # store password_reset record
        auth.password_reset(request.input("email"))
        return "event fired"

    def change_password(self, view: View):  # store password_reset record
        return view.render("auth.change_password")

    def store_changed_password(
        self, auth: Auth, request: Request, response: Response
    ):  # store password_reset record
        auth.reset_password(request.input("password"), request.input("token"))

        # Need to validate??
        # Redirect back?
        return response.back()
