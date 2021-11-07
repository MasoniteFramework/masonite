from src.masonite.providers import Provider
from src.masonite.facades import Gate


class AppProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # Everyone (guests and authenticated users can view posts)
        Gate.define("view-posts", lambda user=None: True)
        Gate.define("display-admin", lambda user: user.email == "admin@gmail.com")

    def boot(self):
        pass
