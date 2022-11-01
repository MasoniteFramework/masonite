import os
from collections import defaultdict
from os.path import relpath, join, basename, isdir, isfile
import shutil
from typing import TYPE_CHECKING

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
from ...utils.str import modularize, as_filepath
from ...utils.filesystem import make_directory
from ..reserved_names import PACKAGE_RESERVED_NAMES
from ..Package import Package

if TYPE_CHECKING:
    from ...foundation import Application
    from ...commands import Command
    from ...presets import Preset


class PackageProvider(Provider):
    """Specific Masonite service provider used in Masonite package ecosystem to easily build a
    package that can register/share config, views, routes, migrations, controllers and assets."""

    vendor_prefix = "vendor"

    def __init__(self, application: "Application"):
        self.application = application
        # TODO: the default here could be set auto by deciding that its the dirname
        # containing the provider !
        self.package = Package()
        self.default_resources: list = ["config", "views", "migrations", "assets"]

    def register(self):
        self.configure()

    def boot(self):
        pass

    # api
    def configure(self):
        """Main method used to configure all resources that need to be registered or published
        by the package."""
        pass

    def publish(self, resources: list, dry: bool = False) -> dict:
        """Publish given packages resources (or all) to the project. If dry is enabled it will just
        show what will be published without publishing it really."""
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

    def root(self, relative_dir: str) -> "PackageProvider":
        """Define python package module root path and absolute package root path.
        It works when installing the package locally with: pip install . or pip install -e .
        and when installing the package from production release with: pip install package-name
        """
        # load module provider
        provider_module = load(self.__module__)
        # get relative module path to package root
        relative_module_path = modularize(relative_dir)
        self.package.module_root = self.__module__[
            0 : self.__module__.find(relative_module_path) + len(relative_module_path)
        ]
        module_root_path = as_filepath(self.package.module_root)
        self.package.abs_root = provider_module.__file__[
            0 : provider_module.__file__.find(module_root_path) + len(module_root_path)
        ]
        return self

    def name(self, name: str) -> "PackageProvider":
        if name in PACKAGE_RESERVED_NAMES:
            raise InvalidPackageName(
                f"{name} is a reserved name. Please choose another name for your package."
            )
        self.package.name = name
        return self

    def vendor_name(self, name: str) -> "PackageProvider":
        """Specify the package vendor name under which resources will be published."""
        self.package.vendor_name = name
        return self

    def config(self, config_filepath: str, publish: bool = False) -> "PackageProvider":
        """Specify package configuration file to be registered in project configuration. You can
        make it publishable by passing publish=True."""
        # TODO: a name must be specified !
        self.package.add_config(config_filepath)
        Config.merge_with(self.package.name, self.package.config)
        if publish:
            self.package.add_publishable_resource(
                "config", config_filepath, config_path(f"{self.package.name}.py")
            )
        return self

    def views(self, location: str, publish: bool = False) -> "PackageProvider":
        """Register views location in the project. location must be a folder containinng the views you want to publish."""
        self.package.add_views(location)
        # register views into project
        self.application.make("view").add_namespaced_location(
            self.package.name, self.package.views
        )

        if publish:
            location_abs_path = self.package._build_path(location)
            for dirpath, _, filenames in os.walk(location_abs_path):
                for f in filenames:
                    # don't add other files than templates
                    view_abs_path = join(dirpath, f)
                    _, ext = os.path.splitext(view_abs_path)
                    if ext != ".html":
                        continue
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

    def commands(self, *commands: "Command") -> "PackageProvider":
        """Register package commands to the project. This will add the package commands into the
        list of Masonite project commands."""
        self.application.make("commands").add(*commands)
        return self

    def presets(self, *presets: "Preset") -> "PackageProvider":
        """Register package presets to the project."""
        for preset in presets:
            self.application.make("presets").add(preset)
        return self

    def migrations(self, *migrations: str) -> "PackageProvider":
        """Register package migrations to the project."""
        self.package.add_migrations(*migrations)
        # use same timestamp for all package migrations
        timestamp = migration_timestamp()
        for index, migration in enumerate(migrations):
            self.package.add_publishable_resource(
                "migrations",
                migration,
                migrations_path(f"{timestamp}{index + 1}_{basename(migration)}"),
            )
        return self

    def routes(self, *routes: str):
        """Register package routes to the project. Controller locations must have been loaded already !"""
        self.package.add_routes(*routes)
        for route_group in self.package.routes:
            self.application.make("router").add(
                Route.group(load(route_group, "ROUTES", []), middleware=["web"])
            )
        return self

    def controllers(self, *controller_locations: str) -> "PackageProvider":
        """Register package controller locations to the project. This will allow to use route
        controller string bindings with controllers from the package inside route definition."""
        self.package.add_controller_locations(*controller_locations)
        Route.add_controller_locations(*self.package.controller_locations)
        return self

    def assets(self, *assets: str) -> "PackageProvider":
        """Register package assets to the project. This will allow the user to publish assets to
        the project."""
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
