"""A Cache Service Provider."""

from config import cache
from masonite import Cache
from masonite.drivers import CacheDiskDriver, CacheRedisDriver
from masonite.managers import CacheManager
from masonite.provider import ServiceProvider


class CacheProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('CacheConfig', cache)
        self.app.bind('CacheDiskDriver', CacheDiskDriver)
        self.app.bind('CacheRedisDriver', CacheRedisDriver)
        self.app.bind('CacheManager', CacheManager(self.app))

    def boot(self, cache: CacheManager):
        self.app.bind('Cache', cache.driver(self.app.make('CacheConfig').DRIVER))
        self.app.swap(Cache, cache.driver(self.app.make('CacheConfig').DRIVER))
