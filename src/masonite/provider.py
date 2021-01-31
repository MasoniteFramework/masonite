"""Module for the Service Provider."""

from .helpers import random_string
from .helpers.filesystem import copy_migration, copy_assets
from .packages import append_or_create_file


class ServiceProvider:
    """Service provider class. Used as mediator for loading objects or entire features into the container."""

    wsgi = True

    def __init__(self):
        """Service provider constructor."""
        self.app = None
        self._publishes = {}
        self._publish_tags = {}

        self._publish_migrations = {}
        self._publish_migrations_tags = {}

        self._publish_assets = {}
        self._publish_assets_tags = {}

    def boot(self):
        """Use to boot things into the container. Typically ran after the register method has been ran."""
        pass

    def register(self):
        """Use to register objects into the container."""
        pass

    def load_app(self, app):
        """Load the container into the service provider.

        Arguments:
            app {masonite.app.App} -- Container object.

        Returns:
            self
        """
        self.app = app
        return self

    def routes(self, routes):
        """Add routes to the container.

        Arguments:
            routes {list} -- List of routes to add to the container
        """
        web_routes = self.app.make("WebRoutes")
        web_routes += routes

    def views(self, views):
        pass

    def http_middleware(self, middleware):
        """Add HTTP middleware to the container.

        Arguments:
            middleware {list} -- List of middleware to add
        """
        http_middleware = self.app.make("HttpMiddleware")
        http_middleware += middleware

    def route_middleware(self, middleware):
        """Add route middleware to the container.

        Arguments:
            middleware {dict} -- A dictionary of route middleware to add
        """
        route_middleware = self.app.make("RouteMiddleware")
        route_middleware.update(middleware)

    def migrations(self, *directories):
        """Add migration directories to the container."""
        for directory in directories:
            self.app.bind("{}_MigrationDirectory".format(random_string(4)), directory)

    def commands(self, *commands):
        """Add commands to the container. Pass in the commands as arguments."""
        for command in commands:
            self.app.bind(
                "{}Command".format(command.__class__.__name__.replace("Command", "")),
                command,
            )

    def assets(self, assets):
        """Add assets to the container.

        Arguments:
            assets {dict} -- A dictionary of assets to add
        """

        self.app.make("staticfiles").update(assets)

    def publishes(self, dictionary, tag=None):
        self._publishes.update(dictionary)
        if tag is not None:
            self._publish_tags.update({tag: dictionary})

    def publishes_assets(self, dictionary, tag=None):
        self._publish_assets.update(dictionary)
        if tag is not None:
            self._publish_assets_tags.update({tag: dictionary})

    def publishes_migrations(self, migrations, tag=None, to="databases/migrations"):
        if tag is not None:
            self._publish_migrations_tags.update({tag: {}})
            for migration in migrations:
                self._publish_migrations_tags[tag].update({migration: to})
        else:
            for migration in migrations:
                self._publish_migrations.update({migration: to})

    def publish(self, tag=None):
        if tag is not None:
            publishing_items = self._publish_tags.get(tag, {})
        else:
            publishing_items = self._publishes

        for from_location, to_location in publishing_items.items():
            append_or_create_file(from_location, to_location)

    def publish_migrations(self, tag=None):
        if tag is not None:
            publishing_items = self._publish_migrations_tags.get(tag, {})
        else:
            publishing_items = self._publish_migrations

        for from_location, to_location in publishing_items.items():
            copy_migration(from_location, to=to_location)

    def publish_assets(self, tag=None):
        if tag is not None:
            publishing_items = self._publish_assets_tags.get(tag, {})
        else:
            publishing_items = self._publish_assets

        for from_location, to_location in publishing_items.items():
            copy_assets(from_location, to=to_location)
