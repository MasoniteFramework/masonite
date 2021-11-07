from ...providers import Provider
from ..helpers.hashid import hashid


class HashIDProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make("view").share({"hashid": hashid})

    def boot(self):
        pass
