from ..AmazonServices import AmazonServices
from ...configuration import config
from ...providers import Provider


class AmazonServicesProvider(Provider):
    wsgi = False

    def register(self):
        services_config = config("amazon.services")

        services = AmazonServices(self.application, services_config)
        self.application.bind("amazon", services)

    def boot(self):
        pass
