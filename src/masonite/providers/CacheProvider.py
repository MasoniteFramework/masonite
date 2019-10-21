"""A Cache Service Provider."""

from .. import Cache
from ..drivers import CacheDiskDriver, CacheRedisDriver
from ..managers import CacheManager
from ..provider import ServiceProvider
from ..helpers import config


class CacheProvider(ServiceProvider):

    wsgi = False

    def register(self):
        # from config import cache
        # self.app.bind('CacheConfig', cache)
        self.app.bind('CacheDiskDriver', CacheDiskDriver)
        self.app.bind('CacheRedisDriver', CacheRedisDriver)
        self.app.bind('CacheManager', CacheManager(self.app))

    def boot(self, cache: CacheManager):
        self.app.bind('Cache', cache.driver(config('cache').DRIVER))
        self.app.swap(Cache, cache.driver(config('cache').DRIVER))
