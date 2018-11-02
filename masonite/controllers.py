"""Module for controllers. Currently not being used."""


class Controller:
    """Base Class for Controllers."""

    def __init__(self):
        """Controller Constructor."""
        self.app = None

    def load_app(self, app):
        """Load the container into the controller.

        Arguments:
            app {masonite.app.App} -- The container object.

        Returns:
            self
        """
        self.app = app
        return self
