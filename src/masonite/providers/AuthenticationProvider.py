from ..authentication import Auth
from ..authentication.guards import WebGuard, TestGuard
from ..configuration import config
from .Provider import Provider


class AuthenticationProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        auth = Auth(self.application).set_configuration(config("auth.guards"))
        auth.add_guard("web", WebGuard(self.application))
        auth.add_guard("test", TestGuard(self.application))
        self.application.bind("auth", auth)

    def boot(self):
        self.application.make("auth").set_user(None)
