from typing import TYPE_CHECKING, Any, Tuple, List

if TYPE_CHECKING:
    from ...foundation import Application


class WebGuard:
    """Web authentication guard to use in classic HTTP requests."""

    def __init__(self, application: "Application"):
        self.application = application

    def set_options(self, options: dict) -> "WebGuard":
        self.options = options
        return self

    def attempt(self, username: str, password: str) -> "Any":
        """Attempt to authenticate the user with the given username/password."""
        attempt = self.options.get("model")().attempt(username, password)
        if attempt and not self.options.get("once"):
            self.application.make("response").cookie("token", attempt.remember_token)
            self.application.make("request").set_user(attempt)
            return attempt

    def get_auth_column(self, username: str) -> str:
        """Get the authentication column."""
        return self.options.get("model")().get_auth_column(username)

    def register(self, dictionary: dict) -> "Any":
        """Register a new user with given data."""
        try:
            register = self.options.get("model")().register(dictionary)
        except Exception:
            return False
        return self.attempt_by_id(register.get_id())

    def user(self) -> "Any|bool":
        """Get the currently logged in user."""
        token = self.application.make("request").cookie("token")
        if token and self.options.get("model")():
            return (
                self.options.get("model")().where("remember_token", token).first()
                or False
            )

        return False

    def attempt_by_id(self, user_id: "str|int"):
        """Attempt to authenticate the user with the given user ID."""
        attempt = self.options.get("model")().attempt_by_id(user_id)

        if attempt and not self.options.get("once"):
            self.application.make("response").cookie("token", attempt.remember_token)
            self.application.make("request").set_user(attempt)
            return attempt

        return False

    def reset_password(self, username: str, new_password: str):
        """Change password of the user with the given username and the new password."""
        attempt = self.options.get("model")().reset_password(username, new_password)

        if attempt:
            return attempt

        return False

    def once(self):
        """Log in the user without saving a cookie.

        Returns:
            self
        """
        self._once = True
        return self

    def logout(self):
        return self
