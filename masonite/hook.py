"""Module for the Hook class."""

from masonite.app import App


class Hook:
    """Hook class is responsible for finding and firing framework hooks."""

    def __init__(self, app: App):
        """Hook constructor.

        Arguments:
            app {masonite.app.App} -- Container object.
        """
        self._app = app

    def fire(self, search):
        """Find all the classes to be fired with the exception hook search string.

        Arguments:
            search {string} -- The search string to collect classes with.
        """
        for key in self._app.collect(search):
            self._app.make(key).load(self._app)
