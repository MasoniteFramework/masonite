"""Password Helper Module."""
import uuid
from ...facades import Hash


class Authenticates:

    __auth__ = "email"
    __password__ = "password"

    def attempt(self, username, password):
        """Attempts to login using a username and password"""
        record = self.where(self.get_username_column(), username).first()
        if not record:
            return False

        record_password = getattr(record, self.get_password_column())
        if not isinstance(record_password, bytes):
            record_password = bytes(record_password or "", "utf-8")
        try:
            if Hash.check(password, record_password):
                record.set_remember_token().save()
                return record
        except ValueError:
            pass

        return False

    def get_auth_column(self, username):
        record = self.where(self.get_username_column(), username).first()
        if not record:
            return False

        return getattr(record, self.get_username_column())

    def register(self, dictionary):
        dictionary.update(
            {self.get_password_column(): Hash.make(dictionary.get("password", ""))}
        )
        return self.create(dictionary)

    def get_id(self):
        return self.get_primary_key_value()

    def attempt_by_id(self, user_id):
        """Attempts to login using a username and password"""
        record = self.find(user_id)
        if not record:
            return False

        record.set_remember_token().save()
        return record

    def get_remember_token(self):
        """Attempts to login using a username and password"""
        return self.remember_token

    def set_remember_token(self, token=None):
        """Attempts to login using a username and password"""
        self.remember_token = str(token) if token else str(uuid.uuid4())
        return self

    def reset_password(self, username, password):
        """Attempts to login using a username and password"""
        self.where(self.get_username_column(), username).update(
            {self.get_password_column(): Hash.make(password)}
        )
        return self

    def get_password_column(self):
        """Attempts to login using a username and password"""
        return self.__password__

    def get_username_column(self):
        """Attempts to login using a username and password"""
        return self.__auth__
