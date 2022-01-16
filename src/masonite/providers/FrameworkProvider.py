from ..foundation import response_handler
from ..request import Request
from ..response import Response
import time


class FrameworkProvider:
    def __init__(self, application):
        self.application = application

    def register(self):
        pass

    def boot(self):
        request = Request(self.application.make("environ"))
        request.app = self.application
        self.application.bind("request", request)
        self.application.bind("response", Response(self.application))
        self.application.bind("start_time", time.time())
