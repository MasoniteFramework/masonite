"""AuthJWTDriver Module."""

import pendulum
from masonite.auth import Auth
from masonite.contracts import AuthContract
from masonite.drivers import BaseDriver
from masonite.exceptions import DriverLibraryNotFound
from masonite.helpers import config, cookie_expire_time
from masonite.request import Request


class AuthJwtDriver(BaseDriver, AuthContract):

    def __init__(self, request: Request):
        """AuthCookieDriver initializer.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
        """
        self.request = request
        try:
            import jwt
            self.jwt = jwt
        except ImportError:
            raise DriverLibraryNotFound("Please install pyjwt by running 'pip install pyjwt'")

    def user(self, auth_model):
        """Gets the user based on this driver implementation

        Arguments:
            auth_model {orator.orm.Model} -- An Orator ORM type object.

        Returns:
            Model|bool
        """
        from config.application import KEY
        if self.request.get_cookie('token'):

            try:
                token = self.jwt.decode(self.request.get_cookie('token'), KEY, algorithms=['HS256'])
            except self.jwt.exceptions.DecodeError:
                self.delete()
                return False

            expired = token['expired']
            token.pop('expired')
            if not pendulum.parse(expired).is_past():
                auth_model = auth_model()
                auth_model.fill(**token)
                return auth_model
            else:
                if config('auth.drivers.jwt.reauthentication', True):
                    auth_model = Auth(self.request).login_by_id(token[auth_model.__primary_key__])
                else:
                    auth_model.fill(**token)

                token.update({
                    'expired': cookie_expire_time(config('auth.drivers.jwt.lifetime', '5 minutes'))
                })
                self.request.cookie('token', token)
                return auth_model
        return False

    def save(self, _, **kwargs):
        """Saves the state of authentication.

        In this case the state is saving to a cookie.

        Arguments:
            remember_token {string} -- A token containing the state.

        Returns:
            bool
        """
        from config.application import KEY
        model = kwargs.get('model', False)
        serialized_dictionary = model.serialize()
        serialized_dictionary.update({
            'expired': cookie_expire_time('5 minutes')
        })
        token = self.jwt.encode(serialized_dictionary, KEY, algorithm='HS256')
        token = bytes(token).decode('utf-8')
        self.request.cookie('token', token)

    def delete(self):
        """Deletes the state depending on the implementation of this driver.

        Returns:
            bool
        """
        self.request.delete_cookie('token')
