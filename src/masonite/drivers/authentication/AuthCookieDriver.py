"""AuthCookieDriver Module."""

from ...contracts import AuthContract
from ...drivers import BaseDriver
from ...app import App


class AuthCookieDriver(BaseDriver, AuthContract):
    def __init__(self, app: App):
        """AuthCookieDriver initializer.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
        """
        self.app = app

    def user(self, auth_model):
        """Gets the user based on this driver implementation

        Arguments:
            auth_model {orator.orm.Model} -- An Orator ORM type object.

        Returns:
            Model|bool
        """
        if self.app.make("Request").get_cookie("token") and auth_model:
            return (
                auth_model.where(
                    "remember_token", self.app.make("Request").get_cookie("token")
                ).first()
                or False
            )

        return False

    def save(self, remember_token, **_):
        """Saves the cookie to some state.

        In this case the state is saving to a cookie.

        Arguments:
            remember_token {string} -- A token containing the state.

        Returns:
            bool
        """
        return self.app.make("Request").cookie("token", remember_token)

    def delete(self):
        """Deletes the state depending on the implementation of this driver.

        Returns:
            bool
        """
        return self.app.make("Request").delete_cookie("token")

    def logout(self):
        """Deletes the state depending on the implementation of this driver.

        Returns:
            bool
        """
        self.delete()
        self.app.make("Request").reset_user()
