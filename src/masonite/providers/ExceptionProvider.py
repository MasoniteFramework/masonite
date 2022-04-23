import builtins

from exceptionite import Handler
from exceptionite.options import DEFAULT_OPTIONS
from exceptionite.renderers import JSONRenderer
from exceptionite.solutions import MasoniteSolutions

from .Provider import Provider
from ..routes import Route
from ..configuration import config
from ..exceptions.ExceptionHandler import ExceptionHandler
from ..dumps import Dumper
from ..exceptions import (
    DumpExceptionHandler,
    HttpExceptionHandler,
    ModelNotFoundHandler,
)
from ..exceptions.exceptionite.controllers import ExceptioniteController
from ..exceptions.exceptionite.tabs import DumpsTab
from ..exceptions.exceptionite.blocks import RequestBlock, AppBlock, ConfigBlock
from ..exceptions.exceptionite import solutions


class ExceptionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        exceptionite = Handler()
        options = config("exceptions")
        # @removed:5.0.0
        # old project won't have new options for exceptions
        if not options.get("options.editor"):
            options = DEFAULT_OPTIONS
        exceptionite.set_options(options)

        # configure exceptionite for Masonite specifically
        exceptionite.app = self.application
        self.application.make("router").add(
            Route.group(
                [
                    Route.post(
                        "/_exceptionite/actions/", ExceptioniteController.run_action
                    )
                ]
            )
        )
        exceptionite.add_renderer("json", JSONRenderer)
        exceptionite.renderer("web").add_tabs(DumpsTab)
        exceptionite.renderer("web").tab("context").add_blocks(
            RequestBlock, AppBlock, ConfigBlock
        )
        exceptionite.renderer("web").tab("solutions").block(
            "possible_solutions"
        ).register(
            solutions.TableNotFound(),
            solutions.MissingCSRFToken(),
            solutions.InvalidCSRFToken(),
            solutions.TemplateNotFound(),
            solutions.NoneResponse(),
            solutions.RouteMiddlewareNotFound(),
            *MasoniteSolutions.get()
        )

        exception_handler = ExceptionHandler(self.application)
        exception_handler.add_driver("exceptionite", exceptionite)
        self.application.bind("exception_handler", exception_handler)

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
        self.application.bind(
            "ModelNotFoundHandler", ModelNotFoundHandler(self.application)
        )

    def boot(self):
        pass
