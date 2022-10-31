from ..providers import Provider

from ..helpers.urls import UrlsHelper
from ..helpers.mix import MixHelper


class HelpersProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.bind("url", UrlsHelper(self.application))
        self.application.bind("mix", MixHelper(self.application))

    def boot(self):
        pass
