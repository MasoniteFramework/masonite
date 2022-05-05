import sys


class Limit:
    _delays_map = {"minute": 1, "hour": 60, "day": 60 * 24}

    def __init__(self, max_attempts: int = 60, delay: int = 1):
        self.max_attempts = max_attempts
        self.delay = delay  # in minutes
        self.key: str = ""

    @classmethod
    def per_minute(cls, max_attempts: int, minutes: int = 1) -> "Limit":
        return cls(max_attempts, minutes)

    @classmethod
    def per_hour(cls, max_attempts: int, hours: int = 1) -> "Limit":
        return cls(max_attempts, 60 * hours)

    @classmethod
    def per_day(cls, max_attempts: int, days: int = 1) -> "Limit":
        return cls(max_attempts, 60 * 24 * days)

    @classmethod
    def from_str(cls, limit: str) -> "Limit":
        max_attempts, delay_key = limit.split("/")
        delay = cls._delays_map.get(delay_key)
        return cls(int(max_attempts), delay)

    @classmethod
    def unlimited(cls) -> "Limit":
        return cls(sys.maxsize)

    def by(self, key: str) -> "Limit":
        self.key = key
        return self

    def is_unlimited(self):
        return self.max_attempts == sys.maxsize
