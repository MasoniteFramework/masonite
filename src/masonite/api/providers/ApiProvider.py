from ...providers import Provider
from ..Api import Api

from ...facades import Config


class ApiProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        api = Api(self.application).set_configuration(Config.get("api.drivers"))
        self.application.bind("api", api)

    def boot(self):
        pass
