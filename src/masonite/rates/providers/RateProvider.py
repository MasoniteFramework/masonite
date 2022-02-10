from ...providers import Provider
from .. import RateLimiter


class RateProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        rate_limiter = RateLimiter(self.application)
        self.application.bind("rate", rate_limiter)

    def boot(self):
        pass
