"""Module for the Service Provider."""

from masonite.helpers import random_string


class ServiceProvider:
    """Service provider class. Used as mediator for loading objects or entire features into the container."""

    wsgi = True

    def __init__(self):
        """Service provider constructor."""
        self.app = None

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
        web_routes = self.app.make('WebRoutes')
        web_routes += routes

    def http_middleware(self, middleware):
        """Add HTTP middleware to the container.

        Arguments:
            middleware {list} -- List of middleware to add
        """
        http_middleware = self.app.make('HttpMiddleware')
        http_middleware += middleware

    def route_middleware(self, middleware):
        """Add route middleware to the container.

        Arguments:
            middleware {dict} -- A dictionary of route middleware to add
        """
        route_middleware = self.app.make('RouteMiddleware')
        route_middleware.update(middleware)

    def migrations(self, *directories):
        """Add migration directories to the container."""
        for directory in directories:
            self.app.bind(
                '{}_MigrationDirectory'.format(random_string(4)),
                directory
            )

    def commands(self, *commands):
        """Add commands to the container. Pass in the commands as arguments."""
        for command in commands:
            self.app.bind(
                '{}Command'.format(command.__class__.__name__.replace('Command', '')),
                command
            )

    def assets(self, assets):
        """Add assets to the container.

        Arguments:
            assets {dict} -- A dictionary of assets to add
        """
        self.app.make('Storage').STATICFILES.update(assets)
