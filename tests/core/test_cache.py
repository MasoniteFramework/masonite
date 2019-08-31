import glob
import os
import time

from config import cache
from masonite.app import App
from masonite.drivers import CacheDiskDriver, CacheRedisDriver
from masonite.environment import LoadEnvironment
from masonite.managers import CacheManager
import unittest

LoadEnvironment()


class TestCache(unittest.TestCase):

    def setUp(self):
        self.app = App()
        # self.app.bind('CacheConfig', cache)
        self.app.bind('CacheDiskDriver', CacheDiskDriver)
        self.app.bind('CacheRedisDriver', CacheRedisDriver)
        self.app.bind('CacheManager', CacheManager(self.app))
        self.app.bind('Application', self.app)
        self.app.bind('Cache', self.app.make('CacheManager').driver('disk'))
        self.drivers = ['disk']
        if os.environ.get('REDIS_CACHE_DRIVER'):
            self.drivers.append('redis')

    def test_driver_disk_cache_store_for(self):
        for driver in self.drivers:
            self.app.bind('Cache', self.app.make(
                'CacheManager').driver(driver))
            key = "cache_driver_test"
            key_store = self.app.make('Cache').store_for(
                key, "macho", 5, "seconds")

            # This return one key like this: cache_driver_test:1519741028.5628147
            self.assertEqual(key, key_store[:len(key)])

            content = self.app.make('Cache').get(key)
            self.assertEqual(content, "macho")
            assert self.app.make('Cache').exists(key)
            assert self.app.make('Cache').is_valid(key)
            self.app.make('Cache').delete(key)

            assert not self.app.make('Cache').is_valid("error")

    def test_driver_disk_cache_store(self):
        for driver in self.drivers:
            self.app.bind('Cache', self.app.make(
                'CacheManager').driver(driver))
            key = "forever_cache_driver_test"
            key = self.app.make('Cache').store(key, "macho")

            # This return the same key because it's forever
            self.assertEqual(key, key)

            content = self.app.make('Cache').get(key)
            self.assertEqual(content, "macho")
            self.assertTrue(self.app.make('Cache').exists(key))
            self.assertTrue(self.app.make('Cache').is_valid(key))
            self.app.make('Cache').delete(key)

    def test_get_cache(self):
        for driver in self.drivers:
            self.app.bind('Cache', self.app.make(
                'CacheManager').driver(driver))

            cache_driver = self.app.make('Cache')

            cache_driver.store('key', 'value')
            self.assertEqual(cache_driver.get('key'), 'value')

            cache_driver.store_for('key_time', 'key value', 4, 'seconds')
            self.assertEqual(cache_driver.get('key_time'), 'key value')

            cache_driver.delete('key')
            cache_driver.delete('key_time')

    def test_cache_expired_before_get(self):
        for driver in self.drivers:
            self.app.bind('Cache', self.app.make(
                'CacheManager').driver(driver))
            cache_driver = self.app.make('Cache')

            cache_driver.store_for('key_for_1_second', 'value', 1, 'second')
            self.assertTrue(cache_driver.is_valid('key_for_1_second'))
            self.assertEqual(cache_driver.get('key_for_1_second'), 'value')

            time.sleep(2)

            self.assertFalse(cache_driver.is_valid('key_for_1_second'))
            self.assertIsNone(cache_driver.get('key_for_1_second'))

            for cache_file in glob.glob('bootstrap/cache/key*'):
                os.remove(cache_file)

    def test_cache_sets_times(self):
        for driver in self.drivers:
            self.app.bind('Cache', self.app.make(
                'CacheManager').driver(driver))

            cache_driver = self.app.make('Cache')

            cache_driver.store_for('key_for_1_minute', 'value', 1, 'minute')
            cache_driver.store_for('key_for_1_hour', 'value', 1, 'hour')
            cache_driver.store_for('key_for_1_day', 'value', 1, 'day')
            cache_driver.store_for('key_for_1_month', 'value', 1, 'month')
            cache_driver.store_for('key_for_1_year', 'value', 1, 'year')

            self.assertTrue(cache_driver.is_valid('key_for_1_minute'))
            self.assertTrue(cache_driver.is_valid('key_for_1_hour'))
            self.assertTrue(cache_driver.is_valid('key_for_1_day'))
            self.assertTrue(cache_driver.is_valid('key_for_1_month'))
            self.assertTrue(cache_driver.is_valid('key_for_1_year'))

            self.assertEqual(cache_driver.get('key_for_1_minute'), 'value')
            self.assertEqual(cache_driver.get('key_for_1_hour'), 'value')
            self.assertEqual(cache_driver.get('key_for_1_day'), 'value')
            self.assertEqual(cache_driver.get('key_for_1_month'), 'value')
            self.assertEqual(cache_driver.get('key_for_1_year'), 'value')

            for cache_file in glob.glob('bootstrap/cache/key*'):
                os.remove(cache_file)
