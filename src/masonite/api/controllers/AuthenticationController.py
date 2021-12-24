from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth
from masonite.api.facades import Api


class AuthenticationController(Controller):
    def auth(self, auth: Auth, request: Request, response: Response):
        user = auth.attempt(request.input("username"), request.input("password"))

        if user:
            return {"data": user.generate_jwt()}

        return response.json(
            {"message": "Could not find username or password"}, status="403"
        )

    def reauth(self, request: Request, response: Response):
        user = Api.attempt_by_token(request.input("token"))

        if user:
            return {"data": user.generate_jwt()}

        return response.json(
            {"message": "Could not reauthenticate based on given token."}, status="403"
        )
