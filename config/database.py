"""Database Settings """
from masonite import env
from masoniteorm.query import QueryBuilder
from masoniteorm.connections import ConnectionResolver


"""
|--------------------------------------------------------------------------
| Databases connectors details
|--------------------------------------------------------------------------
|
| Setup details of the database connectors you want to use.
|
"""

DATABASES = {
    'default': env('DB_CONNECTION', 'sqlite'),
    'sqlite': {
        'driver': 'sqlite',
        'database': env('SQLITE_DB_DATABASE', 'masonite.sqlite3'),
        'prefix': ''
    },
    "mysql": {
        "driver": "mysql",
        "host": env('DB_HOST'),
        "user": env("DB_USERNAME"),
        "password": env("DB_PASSWORD"),
        "database": env("DB_DATABASE"),
        "port": env('DB_PORT'),
        "prefix": "",
        "grammar": "mysql",
        "options": {
            "charset": "utf8mb4",
        },
    },
    "postgres": {
        "driver": "postgres",
        "host": env('DB_HOST'),
        "user": env("DB_USERNAME"),
        "password": env("DB_PASSWORD"),
        "database": env("DB_DATABASE"),
        "port": env('DB_PORT'),
        "prefix": "",
        "grammar": "postgres",
    },
    'mssql': {
        'driver': 'mssql',
        'host': env('MSSQL_DATABASE_HOST'),
        'user': env('MSSQL_DATABASE_USER'),
        'password': env('MSSQL_DATABASE_PASSWORD'),
        'database': env('MSSQL_DATABASE_DATABASE'),
        'port': env('MSSQL_DATABASE_PORT'),
        'prefix': ''
    },
}

ConnectionResolver().set_connection_details(DATABASES)

DB = QueryBuilder(connection_details=DATABASES)
