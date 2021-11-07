from ..exceptions.exceptions import AuthorizationException


class AuthorizationResponse:
    def __init__(self, allowed, message="", status=None):
        self._allowed = allowed
        self.status = status
        self._message = message

    @classmethod
    def allow(cls, message="", status=None):
        return cls(True, message, status)

    @classmethod
    def deny(cls, message="", status=None):
        return cls(False, message, status)

    def allowed(self):
        return self._allowed

    def authorize(self):
        if not self._allowed:
            raise AuthorizationException(self._message, self.status)
        return self

    def get_response(self):
        return self._message, self.status

    def message(self):
        return self._message
