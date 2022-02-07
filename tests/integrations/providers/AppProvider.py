from src.masonite.providers import Provider
from src.masonite.facades import Gate
from src.masonite.facades import Rate


class AppProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # Everyone (guests and authenticated users can view posts)
        Gate.define("view-posts", lambda user=None: True)
        Gate.define("display-admin", lambda user: user.email == "admin@gmail.com")

        # Register rate limits for api
        Rate.register("api", 1)

    def boot(self):
        pass
