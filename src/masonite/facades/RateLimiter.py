from .Facade import Facade


class RateLimiter(metaclass=Facade):
    key = "rate"
