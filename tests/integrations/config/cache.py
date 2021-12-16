"""Cache Config"""

STORES = {
    "default": "local",
    "local": {
        "driver": "file",
        "location": "tests/integrations/storage/framework/cache"
        #
    },
    "redis": {
        "driver": "redis",
        "host": "127.0.0.1",
        "port": "6379",
        "password": "",
        "name": "masonite4",
    },
    "memcache": {
        "driver": "memcache",
        "host": "127.0.0.1",
        "port": "11211",
        "password": "",
        "name": "masonite4",
    },
}
