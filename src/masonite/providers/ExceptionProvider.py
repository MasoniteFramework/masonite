import builtins

from .Provider import Provider
from ..exceptions import ExceptionHandler, DumpExceptionHandler, DD
from ..configuration import config


class ExceptionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        handler = ExceptionHandler(self.application).set_options(config("exceptions"))
        builtins.dd = DD(self.application).dump
        self.application.bind("exception_handler", handler)
        self.application.bind(
            "DumpExceptionHandler", DumpExceptionHandler(self.application)
        )

    def boot(self):
        pass
