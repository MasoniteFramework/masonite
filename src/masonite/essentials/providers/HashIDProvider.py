from ...providers import Provider
from ..helpers.hashid import hashid


class HashIDProvider(Provider):
    """Add HashID feature to the application. This allow to convert IDs back and forth to a hash
    thus avoiding to expose IDs client-side."""

    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make("view").share({"hashid": hashid})

    def boot(self):
        pass
