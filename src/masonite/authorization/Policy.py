from .AuthorizationResponse import AuthorizationResponse


class Policy:
    def allow(self, message="", code=None):
        return AuthorizationResponse.allow(message, code)

    def deny(self, message="", code=None):
        return AuthorizationResponse.deny(message, code)
