"""An AppProvider Service Provider."""

from ..autoload import Autoload
from ..commands import (
    AuthCommand,
    CommandCommand,
    ControllerCommand,
    DownCommand,
    InfoCommand,
    JobCommand,
    KeyCommand,
    MailableCommand,
    MiddlewareCommand,
    ModelCommand,
    ModelDocstringCommand,
    ProviderCommand,
    PublishCommand,
    PresetCommand,
    QueueTableCommand,
    QueueWorkCommand,
    RoutesCommand,
    ServeCommand,
    TestCommand,
    TinkerCommand,
    UpCommand,
    ViewCommand,
)
from ..exception_handler import DumpHandler, ExceptionHandler
from ..helpers import config, load
from ..helpers.routes import flatten_routes
from ..hook import Hook
from ..provider import ServiceProvider
from ..request import Request
from ..response import Response
from ..routes import Route


class AppProvider(ServiceProvider):

    wsgi = True

    def register(self):
        self.app.bind("HookHandler", Hook(self.app))
        self.app.bind("WebRoutes", flatten_routes(load("routes.web.routes")))
        self.app.bind("Route", Route())

        self.app.bind("Container", self.app)

        self.app.bind("ExceptionDumpExceptionHandler", DumpHandler)

        self.app.bind("RouteMiddleware", config("middleware.route_middleware"))
        self.app.bind("HttpMiddleware", config("middleware.http_middleware"))
        self.app.bind("staticfiles", config("storage.staticfiles", {}))

        # Insert Commands
        self._load_commands()

        self._autoload(config("application.autoload"))

    def boot(self, route: Route):
        self.app.bind("Request", Request(self.app.make("Environ")).load_app(self.app))
        self.app.simple(Response(self.app))
        route.load_environ(self.app.make("Environ"))
        self.app.bind("ExceptionHandler", ExceptionHandler(self.app))

    def _autoload(self, directories):
        Autoload(self.app).load(directories)

    def _load_commands(self):
        self.commands(
            AuthCommand(),
            CommandCommand(),
            ControllerCommand(),
            DownCommand(),
            InfoCommand(),
            JobCommand(),
            KeyCommand(),
            MailableCommand(),
            MiddlewareCommand(),
            ModelCommand(),
            ModelDocstringCommand(),
            PresetCommand(),
            ProviderCommand(),
            PublishCommand(),
            QueueWorkCommand(),
            QueueTableCommand(),
            ViewCommand(),
            RoutesCommand(),
            ServeCommand(),
            TestCommand(),
            TinkerCommand(),
            UpCommand(),
        )
