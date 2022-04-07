import time

from ..request import Request
from ..response import Response
from .Provider import Provider

from ..configuration import config
from ..presets.PresetsCapsule import PresetsCapsule
from ..presets import Tailwind, Vue, React, Bootstrap
from ..cors import Cors


class FrameworkProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # @M5 remove this and add PresetsProvider in default project
        presets = PresetsCapsule()
        presets.add(Bootstrap())
        presets.add(Tailwind())
        presets.add(Vue())
        presets.add(React())
        self.application.bind("presets", presets)

        # @M5 remove this and add CorsProvider in default project
        cors = Cors(self.application).set_options(config("cors"))
        self.application.bind("cors", cors)

    def boot(self):
        request = Request(self.application.make("environ"))
        request.app = self.application
        if self.application.has("activate.subdomains") and self.application.make(
            "activate.subdomains"
        ):
            request.activate_subdomains()
        self.application.bind("request", request)
        self.application.bind("response", Response(self.application))

        self.application.bind("start_time", time.time())
