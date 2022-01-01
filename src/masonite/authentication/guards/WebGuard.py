class WebGuard:
    def __init__(self, application):
        self.application = application
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def attempt(self, username, password):
        attempt = self.options.get("model")().attempt(username, password)
        if attempt and not self.options.get("once"):
            self.application.make("response").cookie("token", attempt.remember_token)
            self.application.make("request").set_user(attempt)
            return attempt

    def get_auth_column(self, username):
        return self.options.get("model")().get_auth_column(username)

    def register(self, dictionary):
        try:
            register = self.options.get("model")().register(dictionary)
        except Exception:
            return False
        return self.attempt_by_id(register.get_id())

    def user(self):
        """Get the currently logged in user.

        Returns:
            object|bool -- Returns the current authenticated user object or False or None if there is none.
        """
        token = self.application.make("request").cookie("token")
        if token and self.options.get("model")():
            return (
                self.options.get("model")().where("remember_token", token).first()
                or False
            )

        return False

    def attempt_by_id(self, user_id):
        """Login a user by the user ID.

        Arguments:
            user_id {string|int} -- The ID of the user model record.

        Returns:
            object|False -- Returns the current authenticated user object or False or None if there is none.
        """
        attempt = self.options.get("model")().attempt_by_id(user_id)

        if attempt and not self.options.get("once"):
            self.application.make("response").cookie("token", attempt.remember_token)
            self.application.make("request").set_user(attempt)
            return attempt

        return False

    def reset_password(self, username, new_password):
        """Login a user by the user ID.

        Arguments:
            user_id {string|int} -- The ID of the user model record.

        Returns:
            object|False -- Returns the current authenticated user object or False or None if there is none.
        """
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
