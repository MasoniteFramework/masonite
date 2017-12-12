import uuid
from passlib.hash import pbkdf2_sha256
from peewee import CharField

class PasswordField(CharField):

    def db_value(self, value):
        return pbkdf2_sha256.hash(value)

    def python_value(self, value):
        return value
