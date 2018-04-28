""" An AppProvider Service Provider """
from masonite.commands.AuthCommand import AuthCommand
from masonite.commands.CommandCommand import CommandCommand
from masonite.commands.ControllerCommand import ControllerCommand
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
from masonite.commands.ServeCommand import ServeCommand
from masonite.commands.ViewCommand import ViewCommand
from masonite.exception_handler import ExceptionHandler
from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.routes import Route

from config import storage
from routes import api, web


class AppProvider(ServiceProvider):

    def register(self):
        self.app.bind('WebRoutes', web.ROUTES)
        self.app.bind('Response', None)
        self.app.bind('Storage', storage)
        self.app.bind('Route', Route())
        self.app.bind('Request', Request())
        self.app.bind('Container', self.app)
        self.app.bind('ExceptionHandler', ExceptionHandler(self.app))

        # Insert Commands
        self.app.bind('MasoniteAuthCommand', AuthCommand())
        self.app.bind('MasoniteCommandCommand', CommandCommand())
        self.app.bind('MasoniteControllerCommand', ControllerCommand())
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
        self.app.bind('MasoniteServeCommand', ServeCommand())

    def boot(self, Environ, Request, Route):
        self.app.bind('Headers', [])
        Route.load_environ(Environ)
        Request.load_environ(Environ).load_app(self.app)
