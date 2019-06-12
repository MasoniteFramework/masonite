"""Module for the ache disk driver."""

import os

from masonite.contracts import CacheContract
from masonite.drivers import BaseCacheDriver
from masonite.exceptions import DriverLibraryNotFound


class CacheRedisDriver(CacheContract, BaseCacheDriver):
    """Class for the cache redis driver."""

    def __init__(self):
        """Cache redis driver constructor.

        Arguments:
            CacheConfig {config.cache} -- Cache configuration module.
            Application {config.application} -- Application configuration module.
        """
        from config import application, cache

        self.appconfig = application
        self.cache_forever = None
        self.app_name = os.getenv('APP_NAME', 'masonite')

        config = cache.DRIVERS['redis']

        try:
            import redis
            self.redis = redis
        except ImportError:
            raise DriverLibraryNotFound(
                "Could not find the 'redis' library. Run pip install redis to fix this.")

        self.connection = redis.StrictRedis(
            host=config['host'],
            port=config['port'],
            password=config['password'],
            decode_responses=True)

    def store(self, key, value):
        """Stores content in cache file.

        Arguments:
            key {string} -- The key to store the cache file into
            value {string} -- The value you want to store in the cache

        Keyword Arguments:
            extension {string} -- the extension you want to append to the file (default: {".txt"})
            location {string} -- The path you want to store the cache into. (default: {None})

        Returns:
            string -- Returns the key
        """

        self.cache_forever = True

        self.connection.set('{0}_cache_{1}'.format(self.app_name, key), value)

        return key

    def store_for(self, key, value, cache_time, cache_type):
        """Store the cache for a specific amount of time.

        Arguments:
            key {string} -- The key to store the cache file into
            value {string} -- The value you want to store in the cache
            cache_time {int|string} -- The time as a string or an integer (1, 2, 5, 100, etc)
            cache_type {string} -- The type of time to store for (minute, minutes, hours, seconds, etc)

        Keyword Arguments:
            extension {string} -- the extension you want to append to the file (default: {".txt"})
            location {string} -- The path you want to store the cache into. (default: {None})

        Raises:
            ValueError -- Thrown if an invalid cache type was caught (like houes instead of hours).

        Returns:
            string -- Returns the key
        """

        self.cache_forever = False
        cache_for_time = self.calculate_time(cache_type, cache_time)

        self.connection.set('{0}_cache_{1}'.format(self.app_name, key), value, ex=cache_for_time)

        return key

    def get(self, key):
        """Get the data from a key in the cache."""
        return self.connection.get('{0}_cache_{1}'.format(self.app_name, key))

    def delete(self, key):
        """Delete file cache."""
        self.connection.delete('{0}_cache_{1}'.format(self.app_name, key))

    def update(self, key, value):
        """Updates a specific cache by key."""
        time_to_expire = self.connection.ttl('{0}_cache_{1}'.format(self.app_name, key))

        if time_to_expire > 0:
            self.connection.set('{0}_cache_{1}'.format(self.app_name, key), value, ex=time_to_expire)
        else:
            self.connection.set('{0}_cache_{1}'.format(self.app_name, key), value)

        return key

    def exists(self, key):
        """Check if the cache exists."""
        return self.connection.exists('{0}_cache_{1}'.format(self.app_name, key))

    def is_valid(self, key):
        """Check if a valid cache."""
        return self.exists(key)
