"""Authentication Class."""

import uuid

import bcrypt

from masonite.helpers import password as bcrypt_password, config
from masonite.app import App


class Auth:
    """This class will be used to authenticate users based on the config/auth.py file."""

    _once = False

    def __init__(self, app: App, auth_model=None):
        """Auth constructor.

        Arguments:
            request {masonite.request.Request} -- The Request object.

        Keyword Arguments:
            auth_model {object} -- The model you want to authenticate with (default: {None})
        """
        self.request = app.make('Request')

        if auth_model:
            self.auth_model = auth_model
        else:
            from config import auth
            self.auth_model = auth.AUTH['model']

        self.driver = config('auth.auth.driver', 'cookie')

    def user(self):
        """Get the currently logged in user.

        Raises:
            exception -- Raised when there has been an error handling the user model.

        Returns:
            object|bool -- Returns the current authenticated user object or False or None if there is none.
        """
        try:
            return self.request.app().make('AuthManager').driver(self.driver).user(self.auth_model)
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

            if model and bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self._get_password_column(model), 'utf-8')):
                if not self._once:
                    remember_token = str(uuid.uuid4())
                    model.remember_token = remember_token
                    model.save()
                    self.request.app().make('AuthManager').driver(self.driver).save(remember_token, model=model)
                return model

        except Exception as exception:
            raise exception

        return False

    def logout(self):
        """Logout the current authenticated user.

        Returns:
            self
        """
        self.request.app().make('AuthManager').driver(self.driver).delete()
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
                self.request.app().make('AuthManager').driver(self.driver).save(remember_token, model=model)
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
        self.auth_model.create(**user)
