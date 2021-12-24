from ...providers import Provider
from ..Api import Api

from ...facades import Config
from ...routes import Route
from ...utils.structures import load


class ApiProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        api = Api(self.application).set_configuration(Config.get("api.drivers"))
        self.application.bind("api", api)
        self.application.make("router").add(
            Route.group(
                load(self.application.make("routes.api.location"), "ROUTES"), middleware=["api"], prefix="/api"
            )
        )

    def boot(self):
        pass
