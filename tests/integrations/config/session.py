import os


DRIVERS = {
    "default": "cookie",
    "cookie": {},
    "redis": {
        "host": "127.0.0.1",
        "options": {"db": 1},
        "timeout": 60*60,
        "namespace": "masonite4",
    },
}
