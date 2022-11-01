from typing import TYPE_CHECKING

from ..facades import Api

if TYPE_CHECKING:
    from ...foundation import Application


class JWTGuard:
    def __init__(self, application: "Application"):
        self.application = application

    def set_options(self, options: dict) -> "JWTGuard":
        self.options = options
        return self

    def attempt(self, username: str, password: str):
        """Attempt authentication with given username and password."""
        attempt = self.options.get("model")().attempt(username, password)
        if attempt:
            return attempt

    def get_auth_column(self, username: str):
        """Get configured authentication column."""
        return self.options.get("model")().get_auth_column(username)

    def register(self, dictionary: dict):
        """Register and log in user with given data."""
        try:
            register = self.options.get("model")().register(dictionary)
        except Exception:
            return False
        return self.attempt_by_id(register.get_id())

    def user(self):
        """Get the currently authenticated user."""
        # token = self.application.make("request").cookie("token")
        token = Api.get_token()
        if token and self.options.get("model")():
            return self.options.get("model")().attempt_by_token(token) or False

        return False

    def attempt_by_id(self, user_id: "str|int"):
        """Attempt authentication with the given user ID."""
        attempt = self.options.get("model")().attempt_by_id(user_id)

        if attempt and not self.options.get("once"):
            self.application.make("request").set_user(attempt)
            return attempt

        return False

    def once(self):
        """Log in the user without saving a cookie."""
        # @M5 this is not used
        self._once = True
        return self
