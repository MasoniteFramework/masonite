import builtins

from .Provider import Provider
from ..exceptions import (
    ExceptionHandler,
    DumpExceptionHandler,
    DD,
    HttpExceptionHandler,
)
from ..configuration import config
from ..dumps import Dumper


class ExceptionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        handler = ExceptionHandler(self.application).set_options(config("exceptions"))
        self.application.bind("exception_handler", handler)

        # dumper
        dumper = Dumper(self.application)
        self.application.bind("dumper", dumper)
        builtins.dd = dumper.dd
        builtins.dump = dumper.dump
        builtins.clear_dumps = dumper.clear
        self.application.bind(
            "DumpExceptionHandler", DumpExceptionHandler(self.application)
        )
        self.application.bind(
            "HttpExceptionHandler", HttpExceptionHandler(self.application)
        )

    def boot(self):
        pass
