""" Authentication Class """

import uuid

import bcrypt


class Auth:
    """This class will be used to authenticate users based on the config/auth.py file
    """

    _once = False

    def __init__(self, request, auth_model=None):
        """Auth constructor.

        Arguments:
            request {masonite.request.Request} -- The Request object.

        Keyword Arguments:
            auth_model {object} -- The model you want to authenticate with (default: {None})
        """

        self.request = request

        if auth_model:
            self.auth_model = auth_model
        else:
            from config import auth
            self.auth_model = auth.AUTH['model']

    def user(self):
        """Gets the currently logged in user.

        Raises:
            exception -- Raised when there has been an error handling the user model.

        Returns:
            object|bool -- Returns the current authenticated user object or False or None if there is none.
        """

        try:
            if self.request.get_cookie('token'):
                return self.auth_model.where(
                    'remember_token', self.request.get_cookie('token')
                ).first()

            return False
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

        auth_column = self.auth_model.__auth__
        try:
            model = self.auth_model.where(auth_column, name).first()

            if model and bcrypt.checkpw(bytes(password, 'utf-8'), bytes(model.password, 'utf-8')):
                if not self._once:
                    remember_token = str(uuid.uuid4())
                    model.remember_token = remember_token
                    model.save()
                    self.request.cookie('token', remember_token)
                return model

        except Exception as exception:
            raise exception

        return False

    def logout(self):
        """Logout the current authenticated user.

        Returns:
            self
        """

        self.request.delete_cookie('token')
        return self

    def login_by_id(self, id):
        """Login a user by the user ID.

        Arguments:
            id {string|int} -- The ID of the user model record.

        Returns:
            object|False -- Returns the current authenticated user object or False or None if there is none.
        """

        model = self.auth_model.find(id)

        if model:
            if not self._once:
                remember_token = str(uuid.uuid4())
                model.remember_token = remember_token
                model.save()
                self.request.cookie('token', remember_token)
            return model

        return False

    def once(self):
        """Logs in the user without saving a cookie

        Returns:
            self
        """

        self._once = True
        return self
