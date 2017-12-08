''' A Migrations Database Module '''
from peewee import *
from config import database

db = database.engines['default']

class Migrations(Model):
    migration = CharField(default=255)
    batch = IntegerField(default=0)

    class Meta:
        database = db
        table_name = 'migrations'
