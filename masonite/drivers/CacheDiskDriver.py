import os


class CacheDiskDriver():
    """
    Cache from the disk driver
    """

    def __init__(self, CacheConfig, Application):
        self.config = CacheConfig
        self.appconfig = Application

    def store(self, key, value, location=None):
        if not location:
            location = self.config.DRIVERS['disk']['location']

        location += '/'

        open(os.path.join(location, key), 'w').write(value)

        return key
