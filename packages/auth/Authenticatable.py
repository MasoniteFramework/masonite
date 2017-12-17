''' An authentication model extension '''
from peewee import *

class Authenticatable(Model):
    ''' Used to authenticate users through models '''
    token = CharField(null=True, unique=True)
