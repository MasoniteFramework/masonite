import hashlib


class Limit:
    def __init__(self, max_attempts=60, delay=1):
        self.max_attempts = max_attempts
        self.delay = delay  # in minutes
        self.key = ""

    @classmethod
    def per_minute(cls, max_attempts):
        return cls(max_attempts)

    def get_key(self):
        # if a key has been defined
        if self.key:
            return self.key
        else:
            hashlib.md5(str(self.max_attempts))

    def by(self, key):
        self.key = key
        return self
