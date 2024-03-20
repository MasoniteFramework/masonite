from .Provider import Provider
from ..configuration import config
from ..cors import Cors


class SecurityProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        cors = Cors(self.application).set_options(config("security.cors"))
        self.application.bind("cors", cors)

    def boot(self):
        pass
