from ...providers import Provider
from ..Configuration import Configuration


class ConfigurationProvider(Provider):
    """Add core configuration files management to the application."""

    def __init__(self, application):
        self.application = application

    def register(self):
        config = Configuration(self.application)
        config.load()
        self.application.bind("config", config)

    def boot(self):
        pass
