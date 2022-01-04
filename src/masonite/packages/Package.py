import os
from .PublishableResource import PublishableResource


class Package:
    def __init__(self):
        # absolute root directory to python package root
        self.abs_root = ""
        # relative import path to python package root
        self.module_root = ""
        self.name = ""
        self.abs_config = ""
        self._config = ""
        self.config = ""
        self.commands = []
        self._views = []
        self.views = []
        self._migrations = []
        self.migrations = []
        self._controller_locations = []
        self.controller_locations = []
        self._routes = []
        self.routes = []
        self._assets = []
        self.assets = []
        # all files to be published (can be assets, config, views ..)
        self.files = {}

    def _build_path(self, rel_path):
        """Build absolute path to package file."""
        import pdb

        pdb.set_trace()
        return os.path.join(self.abs_root, rel_path)

    def _build_module_path(self, rel_path):
        """Build relative path to package file."""
        return os.path.join(self.module_root, rel_path)

    def add_config(self, config_path):
        self._config = config_path
        self.config = self._build_module_path(config_path)
        return self

    def add_views(self, *locations):
        for location in locations:
            self._views.append(location)
            self.views.append(self._build_module_path(location))
        return self

    def add_migrations(self, *migrations):
        for migration in migrations:
            self._migrations.append(migration)
            self.migrations.append(self._build_module_path(migration))
        return self

    def add_routes(self, *routes):
        for route in routes:
            self._routes.append(route)
            self.routes.append(self._build_module_path(route))
        return self

    def add_assets(self, *assets):
        for asset in assets:
            self._assets.append(asset)
            self.assets.append(self._build_module_path(asset))
        return self

    def add_controller_locations(self, *controller_locations):
        for loc in controller_locations:
            self._controller_locations.append(loc)
            self.controller_locations.append(self._build_module_path(loc))
        return self

    def add_publishable_resource(self, key, source, abs_destination):
        resource = PublishableResource(key)
        abs_path = self.package._build_path(source)
        resource.add(abs_path, abs_destination)
        self.files.update({resource.key: resource.files})
