from src.masonite.controllers import Controller
from src.masonite.views import View
from tests.integrations.app.User import User
from src.masonite.request import Request
from src.masonite.response import Response
from src.masonite.authentication import Auth


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
