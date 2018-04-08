from masonite.managers.Manager import Manager


class CacheManager(Manager):
    """
    Manager for cache drivers
    """

    config = 'CacheConfig'
    driver_prefix = 'Cache'
