from peewee import *
from config import database
from packages.cashier.Billable import Billable
from packages.extensions.PasswordField import PasswordField

db = database.engines['default']

class Users(Model):
    name = CharField()
    password = PasswordField()

    class Meta:
        database = db
