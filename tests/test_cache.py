from config import cache
from masonite.app import App
from masonite.drivers.CacheDiskDriver import CacheDiskDriver
from masonite.managers.CacheManager import CacheManager
import time


def test_driver_disk_cache_store_for():
    container = App()

    container.bind('CacheConfig', cache)
    container.bind('CacheDiskDriver', CacheDiskDriver)
    container.bind('CacheManager', CacheManager(container))
    container.bind('Application', container)
    container.bind('Cache', container.make('CacheManager').driver('disk'))

    key = "cache_driver_test"
    key_store = container.make('Cache').store_for(key, "macho", 5, "seconds")

    # This return one key like this: cache_driver_test:1519741028.5628147
    assert key == key_store[:len(key)]

    content = container.make('Cache').get(key)
    assert content == "macho"
    assert container.make('Cache').cache_exists(key)
    assert container.make('Cache').is_valid(key)
    container.make('Cache').delete(key)

    assert not container.make('Cache').is_valid("error")


def test_driver_disk_cache_store():
    container = App()

    container.bind('CacheConfig', cache)
    container.bind('CacheDiskDriver', CacheDiskDriver)
    container.bind('CacheManager', CacheManager(container))
    container.bind('Application', container)
    container.bind('Cache', container.make('CacheManager').driver('disk'))

    key = "forever_cache_driver_test"
    key = container.make('Cache').store(key, "macho")

    # This return the same key because it's forever
    assert key == key

    content = container.make('Cache').get(key)
    assert content == "macho"
    assert container.make('Cache').cache_exists(key)
    assert container.make('Cache').is_valid(key)
    container.make('Cache').delete(key)

def test_get_cache():
    container = App()

    container.bind('CacheConfig', cache)
    container.bind('CacheDiskDriver', CacheDiskDriver)
    container.bind('CacheManager', CacheManager(container))
    container.bind('Application', container)
    container.bind('Cache', container.make('CacheManager').driver('disk'))

    cache_driver = container.make('Cache')

    cache_driver.store('key', 'value')

    assert cache_driver.get('key') == 'value'

def test_cache_expired_before_get():
    container = App()

    container.bind('CacheConfig', cache)
    container.bind('CacheDiskDriver', CacheDiskDriver)
    container.bind('CacheManager', CacheManager(container))
    container.bind('Application', container)
    container.bind('Cache', container.make('CacheManager').driver('disk'))

    cache_driver = container.make('Cache')

    cache_driver.store_for('key_for_1_second', 'value', 1, 'second')
    assert cache_driver.is_valid('key_for_1_second')
    assert cache_driver.get('key_for_1_second') == 'value'

    time.sleep(2)

    assert not cache_driver.is_valid('key_for_1_second')
    assert cache_driver.get('key_for_1_second') is None
