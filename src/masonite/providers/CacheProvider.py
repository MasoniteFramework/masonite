from .Provider import Provider
from ..cache import Cache
from ..cache.drivers import FileDriver, RedisDriver, MemcacheDriver
from ..configuration import config


class CacheProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        cache = Cache(self.application).set_configuration(config("cache.stores"))
        cache.add_driver("file", FileDriver(self.application))
        cache.add_driver("redis", RedisDriver(self.application))
        cache.add_driver("memcache", MemcacheDriver(self.application))
        self.application.bind("cache", cache)

    def boot(self):
        pass
