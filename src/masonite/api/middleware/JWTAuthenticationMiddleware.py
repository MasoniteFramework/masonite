from masonite.middleware import Middleware

from masonite.api.facades import Api


class JWTAuthenticationMiddleware(Middleware):
    def before(self, request, response):
        token = Api.get_token()
        if not token:
            return response.json(
                {"message": "Authentication token missing"}, status="401"
            )

        # Check token is not expired
        validate = Api.validate_token(token)
        if not validate:
            return response.json(
                {"message": "Token invalid. Try reauthenticating."}, status=401
            )

        return request

    def after(self, request, response):
        pass
