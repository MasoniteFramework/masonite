"""An AppProvider Service Provider."""

from ..autoload import Autoload
from ..commands import (AuthCommand, CommandCommand, ControllerCommand,
                        DownCommand, InfoCommand, InstallCommand, JobCommand,
                        KeyCommand, MailableCommand, MakeMigrationCommand, MiddlewareCommand,
                        MigrateCommand, MigrateRefreshCommand,
                        MigrateResetCommand, MigrateRollbackCommand,
                        MigrateStatusCommand, ModelCommand,
                        ModelDocstringCommand, ProviderCommand, PublishCommand, PresetCommand,
                        QueueTableCommand, QueueWorkCommand, RoutesCommand,
                        SeedCommand, SeedRunCommand, ServeCommand, TestCommand,
                        TinkerCommand, UpCommand, ViewCommand)
from ..exception_handler import DumpHandler, ExceptionHandler
from ..helpers import config, load
from ..helpers.routes import flatten_routes
from ..hook import Hook
from ..provider import ServiceProvider
from ..request import Request
from ..response import Response
from ..routes import Route


class AppProvider(ServiceProvider):

    def register(self):
        self.app.bind('HookHandler', Hook(self.app))
        self.app.bind('WebRoutes', flatten_routes(load('routes.web.routes')))
        self.app.bind('Route', Route())
        self.app.bind('Request', Request())
        self.app.simple(Response(self.app))
        self.app.bind('Container', self.app)
        self.app.bind('ExceptionHandler', ExceptionHandler(self.app))
        self.app.bind('ExceptionDumpExceptionHandler', DumpHandler)

        self.app.bind('RouteMiddleware', config('middleware.route_middleware'))
        self.app.bind('HttpMiddleware', config('middleware.http_middleware'))
        self.app.bind('staticfiles', config('storage.staticfiles', {}))

        # Insert Commands
        self._load_commands()

        self._autoload(config('application.autoload'))

    def boot(self, request: Request, route: Route):
        self.app.bind('StatusCode', None)
        route.load_environ(self.app.make('Environ'))
        request.load_environ(self.app.make('Environ')).load_app(self.app)

    def _autoload(self, directories):
        Autoload(self.app).load(directories)

    def _load_commands(self):
        self.commands(
            AuthCommand(),
            CommandCommand(),
            ControllerCommand(),
            DownCommand(),
            InfoCommand(),
            InstallCommand(),
            JobCommand(),
            KeyCommand(),
            MailableCommand(),
            MakeMigrationCommand(),
            MiddlewareCommand(),
            MigrateCommand(),
            MigrateRefreshCommand(),
            MigrateResetCommand(),
            MigrateStatusCommand(),
            MigrateRollbackCommand(),
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
            SeedCommand(),
            SeedRunCommand(),
            TestCommand(),
            TinkerCommand(),
            UpCommand()
        )
