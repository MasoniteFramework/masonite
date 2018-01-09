''' Database Settings '''
import os

from dotenv import find_dotenv, load_dotenv
from orator import DatabaseManager, Model

load_dotenv(find_dotenv())

databases = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'masonite',
        'user': 'root',
        'password': '',
        'prefix': ''
    }
}

db = DatabaseManager(databases)
Model.set_connection_resolver(db)
