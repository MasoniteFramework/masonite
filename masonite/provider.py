"""Module for the Service Provider.
"""


class ServiceProvider:
    """Service provider class. Used as mediator for loading objects or entire features into the container.
    """

    wsgi = True

    def __init__(self):
        """Service provider constructor
        """

        self.app = None

    def boot(self):
        """Used to boot things into the container. Typically ran after the register method has been ran.
        """

        pass

    def register(self):
        """Used to register objects into the container.
        """

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
