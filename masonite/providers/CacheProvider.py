""" A Cache Service Provider """

from config import cache
from masonite.drivers import CacheDiskDriver
from masonite.drivers import CacheRedisDriver
from masonite.managers.CacheManager import CacheManager
from masonite.provider import ServiceProvider


class CacheProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('CacheConfig', cache)
        self.app.bind('CacheDiskDriver', CacheDiskDriver)
        self.app.bind('CacheRedisDriver', CacheRedisDriver)
        self.app.bind('CacheManager', CacheManager(self.app))

    def boot(self, CacheManager, CacheConfig):
        self.app.bind('Cache', CacheManager.driver(CacheConfig.DRIVER))
