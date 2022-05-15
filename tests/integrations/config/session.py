import os


DRIVERS = {
    "default": "cookie",
    "cookie": {},
    "redis": {
        "driver_config": {
            "host": "127.0.0.1",
            "port": "6379",
            "password": "",
        },
        "timeout": 60*60,
        "namespace": "masonite4",
    },
}
