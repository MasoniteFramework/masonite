from ...controllers import Controller
from ...request import Request
from ...response import Response
from ...authentication import Auth
from ..facades import Api


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
