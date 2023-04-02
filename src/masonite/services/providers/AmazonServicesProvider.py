from ...configuration import config
from ...providers import Provider
from ..AmazonServices import AmazonServices


class AmazonServicesProvider(Provider):
    wsgi = False

    def register(self):
        services = config("amazon.services", {})
        common = config("amazon.common_config", {})

        services = AmazonServices(self.application, services, common)
        self.application.bind("amazon", services)

    def boot(self):
        pass
