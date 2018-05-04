""" A Cache Service Provider """
from masonite.provider import ServiceProvider
from masonite.managers.CacheManager import CacheManager
from masonite.drivers.CacheDiskDriver import CacheDiskDriver
from config import cache


class CacheProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('CacheConfig', cache)
        self.app.bind('CacheDiskDriver', CacheDiskDriver)
        self.app.bind('CacheManager', CacheManager(self.app))

    def boot(self, CacheManager, CacheConfig):
        self.app.bind('Cache', CacheManager.driver(CacheConfig.DRIVER))
