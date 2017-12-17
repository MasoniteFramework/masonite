from config import database

from peewee import *
from playhouse.fields import PasswordField

from packages.auth.Authenticatable import Authenticatable

db = database.engines['default']

class Users(Authenticatable):
    name = CharField()
    email = CharField(unique=True)
    password = PasswordField()

    class Meta:
        database = db
        auth_column = 'name'
