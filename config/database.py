''' Database Settings '''
import os

from dotenv import find_dotenv, load_dotenv
from orator import DatabaseManager, Model

load_dotenv(find_dotenv())

ENGINES = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'masonite',
        'user': 'root',
        'password': '',
        'prefix': ''
    }
}
