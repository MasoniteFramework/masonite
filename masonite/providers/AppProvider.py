"""An AppProvider Service Provider."""

from masonite.auth import Auth
from masonite.autoload import Autoload
from masonite.commands import (AuthCommand, CommandCommand, ControllerCommand,
                               DownCommand, InfoCommand, InstallCommand,
                               JobCommand, KeyCommand, MakeMigrationCommand,
                               MiddlewareCommand, MigrateCommand,
                               MigrateRefreshCommand, MigrateResetCommand,
                               MigrateRollbackCommand, MigrateStatusCommand,
                               ModelCommand, ModelDocstringCommand,
                               ProviderCommand, PublishCommand,
                               QueueTableCommand, QueueWorkCommand,
                               RoutesCommand, SeedCommand, SeedRunCommand,
                               ServeCommand, TestCommand, TinkerCommand, UpCommand,
                               ViewCommand)
from masonite.exception_handler import DumpHandler, ExceptionHandler
from masonite.helpers import config
from masonite.helpers.routes import flatten_routes
from masonite.hook import Hook
from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.response import Response
from masonite.routes import Route

from masonite.managers import AuthManager
from masonite.drivers import AuthCookieDriver, AuthJwtDriver


class AppProvider(ServiceProvider):

    def register(self):
        from routes import web
        self.app.bind('HookHandler', Hook(self.app))
        self.app.bind('WebRoutes', flatten_routes(web.ROUTES))
        self.app.bind('Storage', config('storage'))
        self.app.bind('Route', Route())
        self.app.bind('Request', Request())
        self.app.simple(Response(self.app))
        self.app.bind('Container', self.app)
        self.app.bind('ExceptionHandler', ExceptionHandler(self.app))
        self.app.bind('ExceptionDumpExceptionHandler', DumpHandler)
        self.app.bind('AuthCookieDriver', AuthCookieDriver)
        self.app.bind('AuthJwtDriver', AuthJwtDriver)
        self.app.bind('AuthManager', AuthManager(self.app).driver('cookie'))
        self.app.bind('RouteMiddleware', config('middleware.route_middleware'))
        self.app.bind('HttpMiddleware', config('middleware.http_middleware'))
        self.app.bind('Auth', Auth)

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
        self.app.bind('MasoniteAuthCommand', AuthCommand())
        self.app.bind('MasoniteCommandCommand', CommandCommand())
        self.app.bind('MasoniteControllerCommand', ControllerCommand())
        self.app.bind('MasoniteDownCommand', DownCommand())
        self.app.bind('MasoniteInfoCommand', InfoCommand())
        self.app.bind('MasoniteInstallCommand', InstallCommand())
        self.app.bind('MasoniteJobCommand', JobCommand())
        self.app.bind('MasoniteKeyCommand', KeyCommand())
        self.app.bind('MasoniteMakeMigrationCommand', MakeMigrationCommand())
        self.app.bind('MasoniteMiddlewareCommand', MiddlewareCommand())
        self.app.bind('MasoniteMigrateCommand', MigrateCommand())
        self.app.bind('MasoniteMigrateRefreshCommand', MigrateRefreshCommand())
        self.app.bind('MasoniteMigrateResetCommand', MigrateResetCommand())
        self.app.bind('MasoniteMigrateStatusCommand', MigrateStatusCommand())
        self.app.bind('MasoniteMigrateRollbackCommand',
                      MigrateRollbackCommand())
        self.app.bind('MasoniteModelCommand', ModelCommand())
        self.app.bind('MasoniteModelDocstringCommand', ModelDocstringCommand())
        self.app.bind('MasoniteProviderCommand', ProviderCommand())
        self.app.bind('MasonitePublishCommand', PublishCommand())
        self.app.bind('MasoniteQueueWorkCommand', QueueWorkCommand())
        self.app.bind('MasoniteQueueTableCommand', QueueTableCommand())
        self.app.bind('MasoniteViewCommand', ViewCommand())
        self.app.bind('MasoniteRoutesCommand', RoutesCommand())
        self.app.bind('MasoniteServeCommand', ServeCommand())
        self.app.bind('MasoniteSeedCommand', SeedCommand())
        self.app.bind('MasoniteSeedRunCommand', SeedRunCommand())
        self.app.bind('MasoniteTestCommand', TestCommand())
        self.app.bind('MasoniteTinkerCommand', TinkerCommand())
        self.app.bind('MasoniteUpCommand', UpCommand())
