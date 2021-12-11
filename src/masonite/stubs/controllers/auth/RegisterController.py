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
        errors = request.validate(
            {
                "email": "required",
                "name": "required",
                "password": "required|strong|confirmed",
            }
        )

        if errors:
            return response.back().with_errors(errors)

        user = auth.register(request.only("name", "email", "password"))

        if not user:
            return response.redirect("/register")

        return response.redirect("/home")
