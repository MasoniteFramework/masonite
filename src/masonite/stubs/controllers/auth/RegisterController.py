from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth


class RegisterController(Controller):
    def show(self, view: View):  # Show register page
        return view.render("auth.register")

    def store(
        self, auth: Auth, request: Request, response: Response
    ):  # store register user
        user = auth.register(request.only("name", "email", "password"))

        if not user:
            return response.redirect("/register")

        return response.redirect("/home")
