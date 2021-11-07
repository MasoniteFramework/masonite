import os


class Package:
    def __init__(self):
        self.root_dir = ""
        self.name = ""
        self.config = ""
        self.commands = []
        self.views = []
        self.migrations = []
        self.controller_locations = []
        self.routes = []
        self.assets = []

    def _build_path(self, rel_path):
        return os.path.join(self.root_dir, rel_path)

    def add_config(self, config_path):
        self.config = self._build_path(config_path)
        return self

    def add_views(self, *locations):
        for location in locations:
            self.views.append(self._build_path(location))
        return self

    def add_migrations(self, *migrations):
        for migration in migrations:
            self.migrations.append(self._build_path(migration))
        return self

    def add_routes(self, *routes):
        for route in routes:
            self.routes.append(self._build_path(route))
        return self

    def add_assets(self, *assets):
        for asset in assets:
            self.assets.append(self._build_path(asset))
        return self

    def add_controller_locations(self, *controller_locations):
        for loc in controller_locations:
            self.controller_locations.append(self._build_path(loc))
        return self
