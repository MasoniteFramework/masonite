DRIVERS = {
    "default": "async",
    "database": {
        "connection": "sqlite",
        "table": "jobs",
        "failed_table": "failed_jobs",
        "attempts": 3,
        "poll": 5,
        "tz": "UTC",
    },
    "redis": {
        #
    },
    # See https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.URLParameters
    # for valid connection options values
    "amqp": {
        "username": "guest",
        "password": "guest",
        "port": "5672",
        "vhost": "",
        "host": "localhost",
        "exchange": "",
        "connection_options": {},
        "channel": "default",
        "queue": "masonite4",
        "tz": "UTC",
        "exchange": "",
    },
    "async": {
        "blocking": True,
        "callback": "handle",
        "mode": "threading",
        "workers": 1,
    },
}
