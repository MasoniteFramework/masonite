from ..guards import JWTGuard
from ..commands.APIInstallCommand import APIInstallCommand
from ...configuration.helpers import config
from ...providers import Provider
from ..Api import Api

from ...routes import Route
from ...utils.structures import load


class ApiProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        api = Api(self.application).set_configuration(config("api.drivers"))
        self.application.bind("api", api)
        self.application.make("router").add(
            Route.group(
                load(self.application.make("routes.api.location"), "ROUTES"),
                middleware=["api"],
                prefix="/api",
            )
        )
        self.application.make("commands").add(APIInstallCommand(self.application))
        self.application.make("auth").add_guard("jwt", JWTGuard(self.application))

    def boot(self):
        pass
