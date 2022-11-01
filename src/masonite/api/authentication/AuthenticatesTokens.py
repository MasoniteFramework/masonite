from ..facades import Api


class AuthenticatesTokens:

    __TOKEN_COLUMN__ = "api_token"

    def generate_jwt(self) -> str:
        token = Api.generate_token()

        setattr(self, self.__TOKEN_COLUMN__, token)
        self.save()
        return token

    def attempt_by_token(self, token: str):
        return self.where(self.__TOKEN_COLUMN__, token).first()
