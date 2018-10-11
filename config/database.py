""" Database Settings """

import os

from masonite import env
from masonite.environment import LoadEnvironment
from orator import DatabaseManager, Model

"""Load Environment Variables
Loads in the environment variables when this page is imported.
"""

LoadEnvironment()

"""Database Settings
Set connection database settings here as a dictionary. Follow the
format below to create additional connection settings.

Supported: 'sqlite', 'mysql', 'postgres'
"""

DATABASES = {
    'default': env('DB_CONNECTION'),
    'sqlite': {
        'driver': 'sqlite',
        'database': env('DB_DATABASE'),
        'prefix': ''
    },
    'mysql': {
        'driver': env('DB_DRIVER'),
        'host': env('DB_HOST'),
        'database': env('DB_DATABASE'),
        'port': env('DB_PORT'),
        'user': env('DB_USERNAME'),
        'password': env('DB_PASSWORD'),
        'prefix': ''
    },
    'postgres': {
        'driver': env('DB_DRIVER'),
        'host': env('DB_HOST'),
        'database': env('DB_DATABASE'),
        'port': env('DB_PORT'),
        'user': env('DB_USERNAME'),
        'password': env('DB_PASSWORD'),
        'prefix': ''
    },
}

DB = DatabaseManager(DATABASES)
Model.set_connection_resolver(DB)
