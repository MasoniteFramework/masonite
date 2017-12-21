''' A User Model '''
from masonite.auth.Authenticatable import Authenticatable
from peewee import CharField
from playhouse.fields import PasswordField

from config import database

db = database.ENGINES['default']

class Users(Authenticatable):
    ''' The User Model. Used for authentication purposes '''
    name = CharField()
    email = CharField(unique=True)
    password = PasswordField()

    class Meta:
        ''' Additional settings for this Model '''
        database = db
        auth_column = 'name'
