import pendulum


class RateLimiter:
    def __init__(self, application):
        self.application = application
        self.limiters = {}

    def register(self, name, callback):
        self.limiters[name] = callback
        return self

    @property
    def cache(self):
        """Get default cache driver"""
        return self.application.make("cache").store()

    def attempts(self, key):
        key = self.clean_key(key)
        return int(self.cache.get(key, default=0))

    def clean_key(self, key):
        """Clean the rate limiter key from unicode characters."""
        if isinstance(key, bytes):
            return key.decode("utf-8")
        return key

    def get_limiter(self, name):
        return self.limiters[name]

    def attempt(self, key, request):
        # limiter = self.limiters[name]
        # limit = limiter.allow(request)
        pass

    def too_many_attempts(self, key, max_attempts):
        key = self.clean_key(key)
        if self.attempts(key) >= max_attempts:
            # trigger remove of cache value if needed
            self.cache.get(f"{key}:timer")
            if self.cache.has(f"{key}:timer"):
                return True
            self.reset_attempts(key)
        return False

    def hit(self, key, delay):
        key = self.clean_key(key)
        # store timestamp when key limit be available again
        available_at = pendulum.now().add(seconds=delay).int_timestamp
        self.cache.add(f"{key}:timer", available_at, delay)
        # ensure key exists
        self.cache.add(key, 0, delay)
        hits = self.cache.increment(key)
        return hits

    def reset_attempts(self, key):
        key = self.clean_key(key)
        return self.cache.forget(key)

    def clear(self, key):
        key = self.clean_key(key)
        self.reset_attempts(key)
        return self.cache.forget(f"{key}:timer")

    def available_at(self, key):
        """Get UNIX timestamp at which key will be available again."""
        key = self.clean_key(key)
        timestamp = int(self.cache.get(f"{key}:timer", 0))
        return timestamp

    def available_in(self, key):
        """Get seconds in which key will be available again."""
        timestamp = self.available_at(key)
        if not timestamp:
            return 0
        else:
            return max(0, timestamp - pendulum.now().int_timestamp)
            # return pendulum.from_timestamp(timestamp).second

    def remaining(self, key, max_attempts):
        key = self.clean_key(key)
        return max_attempts - self.attempts(key)
