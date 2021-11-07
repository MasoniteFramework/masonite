from masoniteorm.connections import ConnectionResolver

DATABASES = {
    "default": "sqlite",
    "sqlite": {
        "driver": "sqlite",
        "database": "database.sqlite3",
    },
}

DB = ConnectionResolver().set_connection_details(DATABASES)
