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
        return self.cache.get(key, default=0)

    def clean_key(self, key):
        """Clean the rate limiter key from unicode characters."""
        # TODO
        return key

    def attempt(self, name, request):
        limiter = self.limiters[name]
        limit = limiter(request)
