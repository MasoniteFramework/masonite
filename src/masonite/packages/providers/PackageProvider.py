import os
from collections import defaultdict
from os.path import relpath, join, basename, isdir, isfile, dirname
import shutil

from ...providers.Provider import Provider
from ...exceptions import InvalidPackageName
from ...utils.location import (
    base_path,
    config_path,
    views_path,
    migrations_path,
    resources_path,
)
from ...facades import Config
from ...utils.time import migration_timestamp
from ...routes import Route
from ...utils.structures import load
from ...utils.filesystem import make_directory

from ..reserved_names import PACKAGE_RESERVED_NAMES
from ..Package import Package


class PackageProvider(Provider):

    vendor_prefix = "vendor"

    def __init__(self, application):
        self.application = application
        # TODO: the default here could be set auto by deciding that its the dirname
        # containing the provider !
        self.package = Package()
        self.default_resources = ["config", "views", "migrations", "assets"]

    def register(self):
        self.configure()

    def boot(self):
        pass

    # api
    def configure(self):
        pass

    def publish(self, resources, dry=False):
        project_root = base_path()
        resources_list = resources or self.default_resources
        published_resources = defaultdict(lambda: [])
        for resource in resources_list:
            resource = self.package.resources.get(resource)
            if not resource:
                continue
            for source, dest in resource.files:
                if not dry:
                    make_directory(dest)
                    shutil.copy(source, dest)
                published_resources[resource.key].append(relpath(dest, project_root))
        return published_resources

    def root(self, relative_dir):
        module = load(relative_dir)
        self.package.module_root = relative_dir
        self.package.abs_root = dirname(module.__file__)
        return self

    def name(self, name):
        if name in PACKAGE_RESERVED_NAMES:
            raise InvalidPackageName(
                f"{name} is a reserved name. Please choose another name for your package."
            )
        self.package.name = name
        return self

    def vendor_name(self, name):
        self.package.vendor_name = name
        return self

    def config(self, config_filepath, publish=False):
        # TODO: a name must be specified !
        self.package.add_config(config_filepath)
        Config.merge_with(self.package.name, self.package.config)
        if publish:
            self.package.add_publishable_resource(
                "config", config_filepath, config_path(f"{self.package.name}.py")
            )
        return self

    def views(self, *locations, publish=False):
        """Register views location in the project.
        locations must be a folder containinng the views you want to publish.
        """
        self.package.add_views(*locations)
        # register views into project
        self.application.make("view").add_namespace(
            self.package.name, self.package.views[0]
        )

        if publish:
            for location in locations:
                location_abs_path = self.package._build_path(location)
                for dirpath, _, filenames in os.walk(location_abs_path):
                    for f in filenames:
                        view_abs_path = join(dirpath, f)
                        self.package.add_publishable_resource(
                            "views",
                            view_abs_path,
                            views_path(
                                join(
                                    self.vendor_prefix,
                                    self.package.name,
                                    relpath(view_abs_path, location_abs_path),
                                )
                            ),
                        )

        return self

    def commands(self, *commands):
        self.application.make("commands").add(*commands)
        return self

    def migrations(self, *migrations):
        self.package.add_migrations(*migrations)
        for migration in migrations:
            self.package.add_publishable_resource(
                "migrations",
                migration,
                migrations_path(f"{migration_timestamp()}_{basename(migration)}"),
            )
        return self

    def routes(self, *routes):
        """Controller locations must have been loaded already !"""
        self.package.add_routes(*routes)
        for route_group in self.package.routes:
            self.application.make("router").add(
                Route.group(load(route_group, "ROUTES", []), middleware=["web"])
            )
        return self

    def controllers(self, *controller_locations):
        self.package.add_controller_locations(*controller_locations)
        Route.add_controller_locations(*self.package.controller_locations)
        return self

    def assets(self, *assets):
        self.package.add_assets(*assets)
        for asset_dir_or_file in assets:
            abs_path = self.package._build_path(asset_dir_or_file)
            if isdir(abs_path):
                for dirpath, _, filenames in os.walk(abs_path):
                    for f in filenames:
                        asset_abs_path = join(dirpath, f)
                        self.package.add_publishable_resource(
                            "assets",
                            asset_abs_path,
                            resources_path(
                                join(
                                    self.vendor_prefix,
                                    self.package.name,
                                    relpath(asset_abs_path, abs_path),
                                )
                            ),
                        )
            elif isfile(abs_path):
                self.package.add_publishable_resource(
                    "assets",
                    abs_path,
                    resources_path(
                        join(
                            self.vendor_prefix,
                            self.package.name,
                            asset_dir_or_file,
                        )
                    ),
                )

        return self
