"""PackageProvider to ease package creations."""
import warnings
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

    def configure(self):
        raise NotImplementedError("configure() should be implemented !")

    def register(self):
        
        package = Package()
        package.name = self._get_name()
        package.base_path = self.get_base_path()

        self.configure(package)

        self._check_name()
        self._check_path()
    
    def boot(self, manager: MailManager):
        
        if self.package.has_config():
            self.publishes(
                {self._get_abs_path(self.config_path): f"config/{self.config_name}.py"},
                tag=self.package.tag_for("config")
            )

        if self.package.has_commands():
            for cmd_name, cmd_class in self.package.commands:
                self.app.bind(
                    "{}Command".format(cmd_name.replace("Command", "")),
                    cmd_class,
                )

        if self.package.has_migrations() and not self._check_migrations_exists():
            migrations = [self._get_abs_path(m) for m in self.package.migrations]
            # TODO: register
            # publish (TODO: check if can pe published with vendor/package prefix)
            self.publishes_migrations(
                migrations,
                tag=self.package.tag("migrations")
            )

        if self.has_assets():
            assets = {self._get_abs_path(rel_path): to_path for rel_path, to_path in self.package.assets}
            self.assets(assets)

        if self.has_routes():
            # register different files containing routes
            routes = []
            for route_path in self.package.routes_paths:
                routes.append(flatten_routes(load(f"{self.name}".{route_path})))

            # TODO: publish

        if self.has_views():


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
            self.package.config_name = basename(config_path)
        self.package.set_tag("config", tag)


    def add_command(self, command, name=None):
        """Add a command to register with an optional name. If not given the name of the class will be used."""
        command_name = name if name else command.__name__
        self.package.commands.append({command_name: Command})
    
    def add_migration(self, migration, tag=None)
        self.migrations.append(migration)

    def add_migrations(self, migrations, tag=None)
        self.migrations += migrations
    
    def add_asset(self, relative_path, publish_name):
        publish_path = join("storage", self.vendor_prefix, self.name, publish_name)
        self.assets.update({relative_path: publish_path})

    def add_assets(self, paths):
        for relative_path, publish_name in paths.items():
            self.add_asset(relative_path, publish_name)

    def add_routes(self, routes):
        if not isinstance(routes, list):
            routes = [routes]
        self.routes_paths += routes

    def add_views(self, views, tag=None):
        pass

    def _check_name(self):
        if not self.package.name:
            raise NotImplementedError("package 'name' should be defined !")
        if "masonite" in self.package.name:
            warnings.warn("'name' in PackageProvider should not contains 'masonite'") 
    
    def _check_path(self):
        if not self.package.base_path:
            raise NotImplementedError("package 'name' should be defined !")

    def _check_migrations_exists(self):
        pass

    def _get_abs_path(self, relative_path):
        return join(self.package.base_path, relative_path)
