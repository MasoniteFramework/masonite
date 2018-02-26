import glob
import os
import re
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

        path_cache = self.config.DRIVERS['disk']['location'] + "/"
        return open(glob.glob(path_cache + key + ':*')[0], 'r').read()

    def delete(self, key):
        """
        Delete file cache
        """

        path_cache = self.config.DRIVERS['disk']['location'] + "/"
        for template in glob.glob(path_cache + key + ':*'):
            os.remove(template)

    def exists_cache(self, key):
        """
        Check if the cache exists
        """
        path = self.config.DRIVERS['disk']['location'] + "/"
        find_template = glob.glob(path + "/" + key + ":*")
        if find_template:
            return True
        return False

    def is_valid(self, key, cache_time, cache_type, extension=".txt"):
        """
        Check if a valid cache
        """

        cache_type = cache_type.lower()
        calc = 0
        if cache_type == "second" or cache_type == "seconds":
            # Set time now for
            calc = 1
        elif cache_type == "minutes" or cache_type == "minute":
            calc = 60
        elif cache_type == "hours" or cache_type == 'hour':
            calc = 60 * 60
        elif cache_type == "days" or cache_type == 'day':
            calc = 60 * 60 * 60
        elif cache_type == "months" or cache_type == 'month':
            calc = 60 * 60 * 60 * 60
        elif cache_type == "years" or cache_type == 'year':
            calc = 60 * 60 * 60 * 60 * 60
        else:
            # If is forever
            return True

        path = self.config.DRIVERS['disk']['location'] + "/"
        find_template = glob.glob(path + "/" + key + ":*")
        if find_template:
            template_file = find_template[0]
        else:
            # Error to find template, then expired
            return False

        time_cache = self.__get_time_cache(key, template_file, extension)

        diff_time = time.time() - float(time_cache)
        cache_for_time = cache_time * calc
        # If diff_time is > cache_for_time is expired
        result = not (diff_time > cache_for_time)
        if not result:
            self.delete(key)
        return result

    def __get_time_cache(self, key, template_file, extension):
        """
        Get time from file cache
        """

        time_cache = re.search(
            key + ":(.*)" + extension, template_file).group(1)
        return float(time_cache)
