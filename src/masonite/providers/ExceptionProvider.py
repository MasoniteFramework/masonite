import builtins

from exceptionite import Handler

from .Provider import Provider
from ..routes import Route
from ..configuration import config
from ..exceptions.ExceptionHandler import ExceptionHandler
from ..dumps import Dumper
from ..exceptions import DumpExceptionHandler, HttpExceptionHandler
from ..exceptions.exceptionite.controllers import ExceptioniteController
from ..exceptions.exceptionite.tabs import DumpsTab
from ..exceptions.exceptionite.blocks import RequestBlock, AppBlock
from ..exceptions.exceptionite import solutions
from ..exceptions.exceptionite.actions import (
    MasoniteDebugAction,
    PostStackOverflowAction,
    CreateMasoniteIssueAction,
)


class ExceptionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        exceptionite = Handler()
        exceptionite.set_options(config("exceptions"))
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
        exceptionite.add_tab(DumpsTab)
        exceptionite.get_tab("context").add_block(RequestBlock).add_block(AppBlock)
        exceptionite.add_action(MasoniteDebugAction)
        exceptionite.add_action(PostStackOverflowAction)
        exceptionite.add_action(CreateMasoniteIssueAction)

        exceptionite.get_tab("solutions").get_block("possible_solutions").register(
            solutions.TableNotFound()
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

    def boot(self):
        pass
