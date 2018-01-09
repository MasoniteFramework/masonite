from orator import DatabaseManager, Model
from config.database import Model

class User(Model):

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'
