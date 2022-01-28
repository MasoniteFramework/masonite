import builtins

from .Provider import Provider
from ..exceptions import ExceptionHandler, DumpExceptionHandler
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
        builtins.dd = dumper.die_and_dump
        builtins.dump = dumper.dump
        self.application.bind(
            "DumpExceptionHandler", DumpExceptionHandler(self.application)
        )

    def boot(self):
        pass
