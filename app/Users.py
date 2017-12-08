from peewee import *
from config import database

db = database.engines['default']

class Users(Model):
    name = CharField() 
    password = CharField() 
    email = CharField() 

    class Meta:
        database = db
