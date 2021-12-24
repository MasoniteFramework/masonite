from ..facades import Api


class AuthenticatesTokens:

    __TOKEN_COLUMN__ = "api_token"

    def generate_jwt(self):
        token = Api.generate_token()

        setattr(self, self.__TOKEN_COLUMN__, token)
        self.save()
        return token

    def attempt_by_token(self, token):
        return self.where(self.__TOKEN_COLUMN__, token).first()
