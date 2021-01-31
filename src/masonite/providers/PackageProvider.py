"""PackageProvider to ease package creations."""
import warnings
from os.path import isdir, isfile, join, basename
from ..helpers.routes import flatten_routes
from ..helpers import load
from ..provider import ServiceProvider


class Package:

    name = ""
    base_path = ""
    config_path = ""
    config_name = ""
    commands = []
    assets = {}
    views = {}
    migrations = []
    routes_paths = []

    tags = {}

    def has_commands(self):
        return len(self.commands) > 0

    def has_config(self):
        return self.config_path != ""

    def has_views(self):
        return len(self.views) > 0

    def has_assets(self):
        return len(self.assets.keys()) > 0

    def has_migrations(self):
        return len(self.migrations) > 0

    def has_routes(self):
        return len(self.routes_paths) > 0

    def tag(self, part):
        return self.tags[part]

    def set_tag(self, part, tag=None):
        tag = tag if tag else f"{self.name}-{part}"
        self.tags.update({part: tag})


class PackageProvider(ServiceProvider):

    wsgi = False
    vendor_prefix = "vendor"
    assets_to = "public"
    part_prefixes = {
        "config": "config",
        "migrations": "migrations",
        "assets": "resources",
        "routes": "routes",
        "views": "templates",
        "commands": "commands",
    }
    package = None

    def configure(self):
        raise NotImplementedError("configure() should be implemented !")

    def register(self):

        self.package = Package()
        self.configure()

        self._check_name()
        self._check_path()

    def boot(self):

        if self.package.has_config():
            self.publishes(
                {
                    self._get_abs_path_dot(
                        self.package.config_path, "config"
                    ): f"config/{self.package.config_name}.py"
                },
                tag=self.package.tag("config"),
            )

        if self.package.has_commands():
            for cmd_name, cmd_class in self.package.commands:
                self.app.bind(
                    "{}Command".format(cmd_name.replace("Command", "")),
                    cmd_class,
                )

        if self.package.has_migrations() and not self._check_migrations_exists():
            migrations = [
                self._get_abs_path_dot(m, "migrations") for m in self.package.migrations
            ]
            self.publishes_migrations(
                migrations,
                to=f"databases/migrations/{self._get_package_namespace()}/",
                tag=self.package.tag("migrations"),
            )

        if self.package.has_assets():
            self.assets(self.package.assets)
            self.publishes_assets(
                self.package.assets,
                tag=self.package.tag("assets"),
            )

        if self.package.has_routes():
            # register different files containing routes
            routes = []
            for route_path in self.package.routes_paths:
                routes.append(flatten_routes(load(f"{self.name}.{route_path}")))

            # TODO: publish

        if self.package.has_views():
            pass

    def inspect(self):
        """Show what is going to be published by this package."""
        pass

    def name(self, name):
        self.package.name = name

    def base_path(self, base_path):
        self.package.base_path = base_path

    def add_config(self, config_path, publish_name=None, tag=None):
        """Define if package have a config file."""
        self.package.config_path = config_path
        if publish_name:
            self.package.config_name = publish_name
        else:
            self.package.config_name = basename(config_path).split(".")[0]
        self.package.set_tag("config", tag)

    def add_command(self, command, name=None):
        """Add a command to register with an optional name. If not given the name of the class will be used."""
        command_name = name if name else command.__name__
        self.package.commands.append({command_name: command})

    def add_migration(self, migration, tag=None):
        self.package.migrations.append(migration)
        self.package.set_tag("migrations", tag)

    def add_migrations(self, migrations, tag=None):
        self.package.migrations += migrations
        self.package.set_tag("migrations", tag)

    def add_asset(self, relative_path, publish_name=None, tag=None):
        from_location = self._get_abs_path(relative_path, "assets")
        name = publish_name if publish_name else basename(relative_path)
        to_location = join(self.assets_to, self._get_package_namespace(), name)
        self.package.assets.update({from_location: to_location})
        self.package.set_tag("assets", tag)

    def add_assets(self, paths={".": None}, tag=None):
        for relative_path, publish_name in paths.items():
            self.add_asset(relative_path, publish_name)
        self.package.set_tag("assets", tag)

    def add_routes(self, routes):
        if not isinstance(routes, list):
            routes = [routes]
        self.routes_paths += routes

    def add_views(self, views, tag=None):
        pass

    def _get_package_namespace(self):
        # TODO: use short name here
        return join(self.vendor_prefix, self.package.name)

    def _check_name(self):
        if not self.package.name:
            raise NotImplementedError("package 'name' should be defined !")
        if "masonite" in self.package.name:
            warnings.warn("'name' in PackageProvider should not contains 'masonite'")

    def _check_path(self):
        if not self.package.base_path:
            raise NotImplementedError("package root 'path' should be defined !")

    def _check_migrations_exists(self):
        pass

    def _get_abs_path(self, relative_path, part):
        # look first in "package" convention location
        path = join(self.package.base_path, self.part_prefixes[part], relative_path)
        if not isfile(path) and not isdir(path):
            # else look at root
            path = join(self.package.base_path, relative_path)

        return path

    def _get_abs_path_dot(self, relative_path, part, ext="py"):
        # add extensions
        if "." in relative_path:
            # resolve given path
            path = load(relative_path)
        else:
            # look first in "package" convention location
            basename = (f"{relative_path}.{ext}",)
            path = join(self.package.base_path, self.part_prefixes[part], basename)
            if not isfile(path) and not isdir(path):
                # else look at root
                path = join(self.package.base_path, basename)
        # TODO: should we check here to returns human exception ?
        return path
