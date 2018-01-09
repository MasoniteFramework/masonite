''' Database Settings '''
import os

from dotenv import find_dotenv, load_dotenv
from orator import DatabaseManager, Model

load_dotenv(find_dotenv())

'''
|--------------------------------------------------------------------------
| Database Settings
|--------------------------------------------------------------------------
|
| Set connection database settings here as a dictionary. Follow the
| format below to create additional connection settings.
|
| @see Orator migrations documentation for more info
|
'''
databases = {
    'mysql': {
        'driver': os.environ.get('DB_DRIVER'),
        'host': os.environ.get('DB_HOST'),
        'database': os.environ.get('DB_DATABASE'),
        'user': os.environ.get('DB_USERNAME'),
        'password': os.environ.get('DB_PASSWORD'),
        'prefix': ''
    }
}

db = DatabaseManager(databases)
Model.set_connection_resolver(db)
