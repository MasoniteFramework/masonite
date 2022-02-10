from src.masonite.providers import Provider
from src.masonite.facades import Gate, RateLimiter
from src.masonite.rates import GuestsOnlyLimiter


class AppProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # Everyone (guests and authenticated users can view posts)
        Gate.define("view-posts", lambda user=None: True)
        Gate.define("display-admin", lambda user: user.email == "admin@gmail.com")

        # Register rate limits for api
        RateLimiter.register("api", GuestsOnlyLimiter("5/hour"))

    def boot(self):
        pass
