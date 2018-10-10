"""A Cache Service Provider."""

from config import cache
from masonite.drivers import CacheDiskDriver
from masonite.managers import CacheManager
from masonite.provider import ServiceProvider
from masonite import Cache


class CacheProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('CacheConfig', cache)
        self.app.bind('CacheDiskDriver', CacheDiskDriver)
        self.app.bind('CacheManager', CacheManager(self.app))

    def boot(self, cache: CacheManager):
        self.app.bind('Cache', cache.driver(self.app.make('CacheConfig').DRIVER))
        self.app.swap(Cache, cache.driver(self.app.make('CacheConfig').DRIVER))
