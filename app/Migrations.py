''' A Migrations Database Module '''
from peewee import Model, CharField, IntegerField
from config import database

db = database.ENGINES['default']

class Migrations(Model):
    ''' Migrations model is responsible for managing the migrations in the database '''
    migration = CharField(default=255)
    batch = IntegerField(default=0)

    class Meta:
        ''' Holds additional model information '''
        database = db
        table_name = 'migrations'
