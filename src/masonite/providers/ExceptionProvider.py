import builtins


from .Provider import Provider
from ..exceptions import (
    ExceptionHandler,
    DumpExceptionHandler,
    DD,
    HttpExceptionHandler,
)
from ..configuration import config
from ..utils.location import views_path


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
        self.application.bind(
            "HttpExceptionHandler", HttpExceptionHandler(self.application)
        )
        self.application.make("view").add_namespaced_location(
            "errors", views_path("errors", absolute=False)
        )

    def boot(self):
        pass
