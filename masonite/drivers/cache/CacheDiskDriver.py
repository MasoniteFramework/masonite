"""Module for the ache disk driver."""

import glob
import os
import time

from masonite.app import App
from masonite.contracts import CacheContract
from masonite.drivers import BaseCacheDriver


class CacheDiskDriver(CacheContract, BaseCacheDriver):
    """Class for the cache disk driver."""

    def __init__(self, app: App):
        """Cache disk driver constructor.

        Arguments:
            CacheConfig {config.cache} -- Cache configuration module.
            Application {config.application} -- Application configuration module.
        """
        self.config = app.make('CacheConfig')
        self.appconfig = app.make('Application')
        self.cache_forever = None

    def store(self, key, value, extension=".txt", location=None):
        """Store content in cache file.

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
        if not location:
            location = self.config.DRIVERS['disk']['location']

        location += '/'
        path = os.path.join(location, key + extension)
        if not os.path.exists(path):
            self._create_directory(path)

        with open(path, 'w') as file:
            file.write(value)

        return key

    def store_for(self, key, value, cache_time, cache_type, extension=".txt", location=None):
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

        cache_for_time = cache_for_time + time.time()

        key = self.store(
            key + ":" + str(cache_for_time),
            value, extension, location
        )

        return key

    def get(self, key):
        """Get the data from a key in the cache."""
        if not self.is_valid(key):
            return None

        cache_path = self.config.DRIVERS['disk']['location'] + "/"
        content = ""

        if self.cache_forever:
            glob_path = cache_path + key + '*'
        else:
            glob_path = cache_path + key + ':*'

        try:
            with open(glob.glob(glob_path)[0], 'r') as file:
                content = file.read()
        except IndexError:
            pass

        return content

    def delete(self, key):
        """Delete file cache."""
        cache_path = self.config.DRIVERS['disk']['location'] + "/"
        if self.cache_forever:
            glob_path = cache_path + key + '*'
        else:
            glob_path = cache_path + key + ':*'

        for template in glob.glob(glob_path):
            os.remove(template)

    def update(self, key, value, location=None):
        """Update a specific cache by key."""
        if not location:
            location = self.config.DRIVERS['disk']['location'] + "/"

        location = os.path.join(location, key)
        cache = glob.glob(location + ':*')[0]

        with open(cache, 'w') as file:
            file.write(str(value))

        return key

    def exists(self, key):
        """Check if the cache exists."""
        cache_path = self.config.DRIVERS['disk']['location'] + "/"
        if self.cache_forever:
            glob_path = cache_path + key + '*'
        else:
            glob_path = cache_path + key + ':*'

        find_template = glob.glob(glob_path)
        if find_template:
            return True
        return False

    def is_valid(self, key):
        """Check if a valid cache."""
        cache_path = self.config.DRIVERS['disk']['location'] + "/"
        if self.cache_forever:
            glob_path = cache_path + key + '*'
        else:
            glob_path = cache_path + key + ':*'

        cache_file = glob.glob(glob_path)
        if cache_file:
            try:
                cache_timestamp = float(
                    os.path.splitext(cache_file[0])[0].split(':')[1]
                )
            except IndexError:
                if self.cache_forever:
                    return True
                else:
                    return False

            if cache_timestamp > time.time():
                return True

        self.delete(key)
        return False

    def _create_directory(self, directory):
        if not os.path.exists(os.path.dirname(directory)):
            # Create the path to the model if it does not exist
            os.makedirs(os.path.dirname(directory))
            return True
        return False
