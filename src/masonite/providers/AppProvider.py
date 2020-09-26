"""An AppProvider Service Provider."""
import os
import importlib
from ..autoload import Autoload
from ..commands import (
    AuthCommand,
    CommandCommand,
    ControllerCommand,
    DownCommand,
    InfoCommand,
    InstallCommand,
    JobCommand,
    KeyCommand,
    MailableCommand,
    MakeMigrationCommand,
    MiddlewareCommand,
    MigrateCommand,
    MigrateRefreshCommand,
    MigrateResetCommand,
    MigrateRollbackCommand,
    MigrateStatusCommand,
    ModelCommand,
    ModelDocstringCommand,
    ProviderCommand,
    PublishCommand,
    PresetCommand,
    QueueTableCommand,
    QueueWorkCommand,
    RoutesCommand,
    SeedCommand,
    SeedRunCommand,
    ServeCommand,
    TestCommand,
    TinkerCommand,
    UpCommand,
    ViewCommand,
)
from ..exception_handler import DumpHandler, ExceptionHandler
from ..helpers import config, load, Dot
from ..helpers.routes import flatten_routes
from ..hook import Hook
from ..provider import ServiceProvider
from ..request import Request
from ..response import Response
from ..routes import Route
from ..config import ConfigRepository


class AppProvider(ServiceProvider):
    def register(self):

        config_repo = ConfigRepository()
        self.app.bind("Config", config_repo)
        self._load_config_files(config_repo)
    
        self.app.bind("HookHandler", Hook(self.app))
        self.app.bind("WebRoutes", flatten_routes(load("routes.web.routes")))
        self.app.bind("Route", Route())
        self.app.bind("Request", Request())
        self.app.simple(Response(self.app))
        self.app.bind("Container", self.app)
        self.app.bind("ExceptionHandler", ExceptionHandler(self.app))
        self.app.bind("ExceptionDumpExceptionHandler", DumpHandler)

        self.app.bind("RouteMiddleware", config("middleware.route_middleware"))
        self.app.bind("HttpMiddleware", config("middleware.http_middleware"))
        self.app.bind("staticfiles", config("storage.staticfiles", {}))

        # Insert Commands
        self._load_commands()
        import pdb
        pdb.set_trace()
        self._autoload(config("application.autoload"))

    def boot(self, request: Request, route: Route):
        self.app.bind("StatusCode", None)
        route.load_environ(self.app.make("Environ"))
        request.load_environ(self.app.make("Environ")).load_app(self.app)

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
            UpCommand(),
        )

    def _load_config_files(self, repository):
        files = self._get_config_files()

        if files.get("app", None):
            raise Exception("Unable to load the 'app' configuration file.")

        for config_name, config_path in files.items():
            config_attrs = {}
            # TODO: get attributes of config file as dict
            m = importlib.import_module("config." + config_name)
            config_vars = []
            for var in dir(m):
                if not var.startswith("__") and var.isupper():
                    config_vars.append(var)
            for attr in config_vars:
                attr_name = attr
                # attr_name = attr.lower()
                value = Dot().locate("config." + config_name + "." + attr_name)
                if isinstance(value, dict):
                    values_dict = Dot().flatten(value)
                    config_attrs[attr_name] = values_dict
                else:
                    config_attrs[attr_name] = value
            repository._set(config_name, config_attrs)


    def _get_config_files(self):
        """Get all configuration files for the application"""
        config_files = {}
        config_directory = os.path.join(os.getcwd(), "config")
        for root, dirs, files in os.walk(config_directory):
            for file in files:
                if file.endswith(".py") and os.path.basename(file) != "__init__.py":
                    name = os.path.splitext(os.path.basename(file))[0]
                    config_files[name] = os.path.join(root, file)

        return config_files
