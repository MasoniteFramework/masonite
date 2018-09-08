""" Cache Manager """

from masonite.contracts import CacheManagerContract
from masonite.managers import Manager


class CacheManager(Manager, CacheManagerContract):
    """Manages all cache drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'CacheConfig'
    driver_prefix = 'Cache'
