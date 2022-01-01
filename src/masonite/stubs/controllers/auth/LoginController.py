from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth


class LoginController(Controller):
    def show(self, view: View):
        return view.render("auth.login")

    def store(self, request: Request, auth: Auth, response: Response):
        login = auth.attempt(request.input("username"), request.input("password"))

        if login:
            return response.redirect(name="auth.home")

        # Go back to login page
        return response.redirect(name="login").with_errors(
            ["The email or password is incorrect"]
        )

    def logout(self, auth: Auth, response: Response):
        auth.logout()
        return response.redirect(name="login")
