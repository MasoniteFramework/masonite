import sys


class Limit:
    _delays_map = {"minute": 1, "hour": 60, "day": 60 * 24}

    def __init__(self, max_attempts=60, delay=1):
        self.max_attempts = max_attempts
        self.delay = delay  # in minutes
        self.key = ""

    @classmethod
    def per_minute(cls, max_attempts, minutes=1):
        return cls(max_attempts, minutes)

    @classmethod
    def per_hour(cls, max_attempts, hours=1):
        return cls(max_attempts, 60 * hours)

    @classmethod
    def per_day(cls, max_attempts, days=1):
        return cls(max_attempts, 60 * 24 * days)

    @classmethod
    def from_str(cls, limit):
        max_attempts, delay_key = limit.split("/")
        delay = cls._delays_map.get(delay_key)
        return cls(int(max_attempts), delay)

    @classmethod
    def unlimited(cls):
        return cls(sys.maxsize)

    def by(self, key):
        self.key = key
        return self
