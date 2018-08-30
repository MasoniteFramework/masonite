""" Cache Manager """

from masonite.managers.Manager import Manager


class CacheManager(Manager):
    """Manages all cache drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'CacheConfig'
    driver_prefix = 'Cache'
