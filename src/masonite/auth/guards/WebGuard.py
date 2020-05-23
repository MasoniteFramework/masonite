import uuid

import bcrypt

from ...app import App
from ...request import Request
from ...drivers import AuthCookieDriver, AuthJwtDriver
from ...helpers import config
from ...helpers import password as bcrypt_password
from .AuthenticationGuard import AuthenticationGuard


class WebGuard(AuthenticationGuard):

    drivers = {
        'cookie': AuthCookieDriver,
        'jwt': AuthJwtDriver
    }

    def __init__(self, app: App, request: Request, driver=None, auth_model=None):
        self.app = app
        self.request = request
        self._once = False
        self.auth_model = auth_model or config('auth.auth.guards.web.model')
        self.driver = self.make(driver or config('auth.auth.guards.web.driver'))

    def user(self):
        """Get the currently logged in user.

        Raises:
            exception -- Raised when there has been an error handling the user model.

        Returns:
            object|bool -- Returns the current authenticated user object or False or None if there is none.
        """
        try:
            return self.driver.user(self.auth_model)
        except Exception as exception:
            raise exception

        return None

    def login(self, name, password):
        """Login the user based on the parameters provided.

        Arguments:
            name {string} -- The field to authenticate. This could be a username or email address.
            password {string} -- The password to authenticate with.

        Raises:
            exception -- Raised when there has been an error handling the user model.

        Returns:
            object|bool -- Returns the current authenticated user object or False or None if there is none.
        """

        if not isinstance(password, str):
            raise TypeError("Cannot login with password '{}' of type: {}".format(password, type(password)))

        auth_column = self.auth_model.__auth__

        try:
            # Try to login multiple or statements if given an auth list
            if isinstance(auth_column, list):
                model = self.auth_model.where(auth_column[0], name)

                for authentication_column in auth_column[1:]:
                    model.or_where(authentication_column, name)

                model = model.first()
            else:
                model = self.auth_model.where(auth_column, name).first()

            # MariaDB/MySQL can store the password as string
            # while PostgreSQL can store it as bytes
            # This is to prevent to double encode the password as bytes
            password_as_bytes = self._get_password_column(model)
            if not isinstance(password_as_bytes, bytes):
                password_as_bytes = bytes(password_as_bytes or '', 'utf-8')

            if model and bcrypt.checkpw(bytes(password, 'utf-8'), password_as_bytes):
                if not self._once:
                    remember_token = str(uuid.uuid4())
                    model.remember_token = remember_token
                    model.save()
                    self.driver.save(remember_token, model=model)

                self.request.set_user(model)
                return model

        except Exception as exception:
            raise exception

        return False

    def logout(self):
        """Logout the current authenticated user.

        Returns:
            self
        """
        self.driver.logout()
        return self

    def login_by_id(self, user_id):
        """Login a user by the user ID.

        Arguments:
            user_id {string|int} -- The ID of the user model record.

        Returns:
            object|False -- Returns the current authenticated user object or False or None if there is none.
        """
        model = self.auth_model.find(user_id)

        if model:
            if not self._once:
                remember_token = str(uuid.uuid4())
                model.remember_token = remember_token
                model.save()
                self.driver.save(remember_token, model=model)
            self.request.set_user(model)
            return model

        return False

    def once(self):
        """Log in the user without saving a cookie.

        Returns:
            self
        """
        self._once = True
        return self

    def _get_password_column(self, model):
        """Gets the password column to use.

        Arguments:
            model {orator.orm.Model} -- An Orator type model.

        Returns:
            string
        """
        if hasattr(model, '__password__'):
            return getattr(model, model.__password__)

        if hasattr(model, 'password'):
            return getattr(model, 'password')

    def register(self, user):
        """Register the user.

        Arguments:
            user {dict} -- A dictionary of user data information.
        """
        user['password'] = bcrypt_password(user['password'])
        return self.auth_model.create(**user)
