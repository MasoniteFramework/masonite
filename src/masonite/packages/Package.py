import os

from .PublishableResource import PublishableResource


class Package:
    def __init__(self):
        # absolute root directory to python package root
        self.abs_root = ""
        # relative import path to python package root
        self.module_root = ""
        self.name = ""
        self.config = ""
        self.commands = []
        self.views = []
        self.migrations = []
        self.controller_locations = []
        self.routes = []
        self.assets = []
        # all files to be published (can be assets, config, views...)
        self.resources = {}

    def _build_path(self, rel_path):
        """Build absolute path to package file."""
        return os.path.join(self.abs_root, rel_path)

    def _build_module_path(self, rel_path):
        """Build relative path to package file."""
        return os.path.join(self.module_root, rel_path)

    def add_config(self, config_path):
        self.config = self._build_module_path(config_path)
        return self

    def add_views(self, location):
        views_folder = self._build_module_path(location)
        if not os.path.isdir(self._build_path(location)):
            raise ValueError(
                "views() first argument must be a folder containing all package views."
            )
        self.views = views_folder
        return self

    def add_migrations(self, *migrations):
        for migration in migrations:
            self.migrations.append(self._build_module_path(migration))
        return self

    def add_routes(self, *routes):
        for route in routes:
            self.routes.append(self._build_module_path(route))
        return self

    def add_assets(self, *assets):
        for asset in assets:
            self.assets.append(self._build_module_path(asset))
        return self

    def add_controller_locations(self, *controller_locations):
        for loc in controller_locations:
            self.controller_locations.append(self._build_module_path(loc))
        return self

    def add_publishable_resource(self, key, source, abs_destination):
        resource = self.resources.get(key, None) or PublishableResource(key)
        abs_path = self._build_path(source)
        resource.add(abs_path, abs_destination)
        self.resources.update({key: resource})
