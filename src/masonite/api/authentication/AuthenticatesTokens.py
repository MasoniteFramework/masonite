from ..facades import Api


class AuthenticatesTokens:

    __TOKEN_COLUMN__ = "api_token"

    def generate_jwt(self):
        token = Api.generate_token(self)

        setattr(self, self.__TOKEN_COLUMN__, token)
        self.save()
        return token
