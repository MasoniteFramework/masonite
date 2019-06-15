"""Base cache driver module."""

from masonite.drivers import BaseDriver


class BaseCacheDriver(BaseDriver):
    """Base class that all cache drivers inherit from."""

    def calculate_time(self, cache_type, cache_time):
        """Convert time to required unit
        Returns:
            self
        """

        cache_type = cache_type.lower()
        calc = 0

        if cache_type in ("second", "seconds"):
            # Set time now for
            calc = 1
        elif cache_type in ("minute", "minutes"):
            calc = 60
        elif cache_type in ("hour", "hours"):
            calc = 60 ** 2
        elif cache_type in ("day", "days"):
            calc = 60 ** 3
        elif cache_type in ("month", "months"):
            calc = 60 ** 4
        elif cache_type in ("year", "years"):
            calc = 60 ** 5
        else:
            raise ValueError(
                '{0} is not a valid caching type.'.format(cache_type))

        return cache_time * calc
