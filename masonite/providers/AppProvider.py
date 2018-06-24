""" An AppProvider Service Provider """
from masonite.commands.AuthCommand import AuthCommand
from masonite.commands.CommandCommand import CommandCommand
from masonite.commands.ControllerCommand import ControllerCommand
from masonite.commands.InfoCommand import InfoCommand
from masonite.commands.InstallCommand import InstallCommand
from masonite.commands.JobCommand import JobCommand
from masonite.commands.KeyCommand import KeyCommand
from masonite.commands.MakeMigrationCommand import MakeMigrationCommand
from masonite.commands.MigrateCommand import MigrateCommand
from masonite.commands.MigrateRefreshCommand import MigrateRefreshCommand
from masonite.commands.MigrateResetCommand import MigrateResetCommand
from masonite.commands.MigrateRollbackCommand import MigrateRollbackCommand
from masonite.commands.ModelCommand import ModelCommand
from masonite.commands.ProviderCommand import ProviderCommand
from masonite.commands.RoutesCommand import RoutesCommand
from masonite.commands.ServeCommand import ServeCommand
from masonite.commands.SeedCommand import SeedCommand
from masonite.commands.SeedRunCommand import SeedRunCommand
from masonite.commands.TinkerCommand import TinkerCommand
from masonite.commands.ViewCommand import ViewCommand
from masonite.exception_handler import ExceptionHandler
from masonite.helpers.routes import flatten_routes
from masonite.hook import Hook
from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.routes import Route

from config import storage, application, middleware
from masonite.autoload import Autoload
from routes import api, web

class AppProvider(ServiceProvider):

    def register(self):
        self.app.bind('HookHandler', Hook(self.app))
        self.app.bind('WebRoutes', flatten_routes(web.ROUTES))
        self.app.bind('Response', None)
        self.app.bind('Storage', storage)
        self.app.bind('Route', Route())
        self.app.bind('Request', Request())
        self.app.bind('Container', self.app)
        self.app.bind('ExceptionHandler', ExceptionHandler(self.app))
        self.app.bind('RouteMiddleware', middleware.ROUTE_MIDDLEWARE)

        # Insert Commands
        self.app.bind('MasoniteAuthCommand', AuthCommand())
        self.app.bind('MasoniteCommandCommand', CommandCommand())
        self.app.bind('MasoniteControllerCommand', ControllerCommand())
        self.app.bind('MasoniteInfoCommand', InfoCommand())
        self.app.bind('MasoniteInstallCommand', InstallCommand())
        self.app.bind('MasoniteJobCommand', JobCommand())
        self.app.bind('MasoniteKeyCommand', KeyCommand())
        self.app.bind('MasoniteMakeMigrationCommand', MakeMigrationCommand())
        self.app.bind('MasoniteMigrateCommand', MigrateCommand())
        self.app.bind('MasoniteMigrateRefreshCommand', MigrateRefreshCommand())
        self.app.bind('MasoniteMigrateResetCommand', MigrateResetCommand())
        self.app.bind('MasoniteMigrateRollbackCommand', MigrateRollbackCommand())
        self.app.bind('MasoniteModelCommand', ModelCommand())
        self.app.bind('MasoniteProviderCommand', ProviderCommand())
        self.app.bind('MasoniteViewCommand', ViewCommand())
        self.app.bind('MasoniteRoutesCommand', RoutesCommand())
        self.app.bind('MasoniteServeCommand', ServeCommand())
        self.app.bind('MasoniteSeedCommand', SeedCommand())
        self.app.bind('MasoniteSeedRunCommand', SeedRunCommand())
        self.app.bind('MasoniteTinkerCommand', TinkerCommand())

        self._autoload(application.AUTOLOAD)

    def boot(self, Environ, Request, Route):
        self.app.bind('Headers', [])
        self.app.bind('StatusCode', '404 Not Found')
        Route.load_environ(Environ)
        Request.load_environ(Environ).load_app(self.app)

    def _autoload(self, directories):
        Autoload(self.app).load(directories)
