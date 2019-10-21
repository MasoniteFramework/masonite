"""Cache Manager."""

from ..contracts import CacheManagerContract
from .Manager import Manager


class CacheManager(Manager, CacheManagerContract):
    """Manages all cache drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'cache'
    driver_prefix = 'Cache'


class Cache:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
