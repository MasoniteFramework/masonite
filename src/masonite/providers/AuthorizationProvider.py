from ..authorization import Gate
from .Provider import Provider


class AuthorizationProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.bind("gate", Gate(self.application))

    def boot(self):
        pass
