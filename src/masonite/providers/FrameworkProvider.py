import time

from ..request import Request
from .Provider import Provider


class FrameworkProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        pass

    def boot(self):
        from ..response import Response

        request = Request(self.application.make("environ"))
        request.app = self.application
        if self.application.has("activate.subdomains") and self.application.make(
            "activate.subdomains"
        ):
            request.activate_subdomains()
        self.application.bind("request", request)
        self.application.bind("response", Response(self.application))

        self.application.bind("start_time", time.time())
