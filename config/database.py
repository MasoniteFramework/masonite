import os

from masonite.orm.builder.QueryBuilder import QueryBuilder

from config.database import QueryBuilder
from src.masonite.environment import LoadEnvironment, env

"""
|--------------------------------------------------------------------------
| Load Environment Variables
|--------------------------------------------------------------------------
|
| Loads in the environment variables when this page is imported.
|
"""

LoadEnvironment()

"""
The connections here don't determine the database but determine the "connection".
They can be named whatever you want.
"""

DATABASES = {
    'default': env('DB_CONNECTION', 'sqlite'),
    'sqlite': {
        'driver': 'sqlite',
        'database': env('SQLITE_DB_DATABASE', 'masonite.db'),
        'log_queries': env('DB_LOG'),
        'prefix': ''
    },
    'mysql': {
        'driver': 'mysql',
        'host': env('DB_HOST'),
        'database': env('DB_DATABASE'),
        'port': env('DB_PORT'),
        'user': env('DB_USERNAME'),
        'password': env('DB_PASSWORD'),
        'log_queries': env('DB_LOG'),
    },
    'postgres': {
        'driver': 'postgres',
        'host': env('DB_HOST'),
        'database': env('DB_DATABASE'),
        'port': env('DB_PORT'),
        'user': env('DB_USERNAME'),
        'password': env('DB_PASSWORD'),
        'log_queries': env('DB_LOG'),
    },
}

DB = QueryBuilder(connection_details=DATABASES)