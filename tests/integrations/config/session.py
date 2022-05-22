import os


DRIVERS = {
    "default": "cookie",
    "cookie": {},
    "redis": {
        "host": "127.0.0.1",
        "port": 6379,
        "password": "",
        "options": {"db": 1}, # redis module driver specific options
        "timeout": 60*60,
        "namespace": "masonite4",
    },
}
