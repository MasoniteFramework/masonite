import glob
import os
import time


class CacheDiskDriver():
    """
    Cache from the disk driver
    """

    def __init__(self, CacheConfig, Application):
        self.config = CacheConfig
        self.appconfig = Application

    def store(self, key, value, extension=".txt", location=None):
        """
        Store content in cache file
        """

        if not location:
            location = self.config.DRIVERS['disk']['location']

        location += '/'

        open(os.path.join(location, key + extension), 'w').write(value)

        return key

    def get(self, key):
        """
        Get the data from a key in the cache
        """

        cache_path = self.config.DRIVERS['disk']['location'] + "/"
        return open(glob.glob(cache_path + key + ':*')[0], 'r').read()

    def delete(self, key):
        """
        Delete file cache
        """

        cache_path = self.config.DRIVERS['disk']['location'] + "/"
        for template in glob.glob(cache_path + key + ':*'):
            os.remove(template)

    def cache_exists(self, key):
        """
        Check if the cache exists
        """
        path = self.config.DRIVERS['disk']['location'] + "/"
        find_template = glob.glob(path + "/" + key + ":*")
        if find_template:
            return True
        return False

    def is_valid(self, key):
        """
        Check if a valid cache
        """
        path = self.config.DRIVERS['disk']['location'] + "/"
        cache_file = glob.glob(path + key + ':*')
        if cache_file:
            cache_timestamp = float(
                os.path.splitext(cache_file[0])[0].split(':')[1]
            )
            if cache_timestamp > time.time():
                return True

        self.delete(key)
        return False
