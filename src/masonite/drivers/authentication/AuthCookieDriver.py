"""AuthCookieDriver Module."""

from masonite.contracts import AuthContract
from masonite.drivers import BaseDriver
from masonite.request import Request


class AuthCookieDriver(BaseDriver, AuthContract):

    def __init__(self, request: Request):
        """AuthCookieDriver initializer.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
        """
        self.request = request

    def user(self, auth_model):
        """Gets the user based on this driver implementation

        Arguments:
            auth_model {orator.orm.Model} -- An Orator ORM type object.

        Returns:
            Model|bool
        """
        if self.request.get_cookie('token') and auth_model:
            return auth_model.where(
                'remember_token', self.request.get_cookie('token')
            ).first()

        return False

    def save(self, remember_token, **_):
        """Saves the cookie to some state.

        In this case the state is saving to a cookie.

        Arguments:
            remember_token {string} -- A token containing the state.

        Returns:
            bool
        """
        return self.request.cookie('token', remember_token)

    def delete(self):
        """Deletes the state depending on the implementation of this driver.

        Returns:
            bool
        """
        return self.request.delete_cookie('token')
