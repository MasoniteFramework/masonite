"""A Guard Class Module."""
from ...app import App
from ...exceptions import DriverNotFound


class Guard:

    guards = {}

    def __init__(self, app: App):
        """Guard Initializer

        Arguments:
            app {masonite.app.App} -- The Masonite container
        """
        self.app = app

    def make(self, key):
        """Makes a guard that has been previously registered

        Arguments:
            key {string} -- The key of the guard to fetch.

        Raises:
            DriverNotFound: Raised when trying to fetch a guard that has not been registered yet.

        Returns:
            [type] -- [description]
        """
        if key in self.guards:
            self._guard = self.app.resolve(self.guards[key])
            return self._guard

        raise DriverNotFound("Could not find the guard: '{}'".format(key))

    def guard(self, key):
        """Alias for the make method.

        Arguments:
            key {string} -- The key of the guard to fetch.

        Returns:
            masonite.guards.* -- An instance of a guard class.
        """
        return self.make(key)

    def set(self, key):
        """Sets the specified guard as the default guard to use.

        Arguments:
            key {string} -- The key of the guard to set.

        Returns:
            masonite.guards.* -- An instance of guard class.
        """
        return self.make(key)

    def get(self):
        """Gets the guard current class.

        Returns:
            masonite.guards.* -- An instance of guard class.
        """
        return self._guard

    def driver(self, key):
        """Gets the driver for the currently set guard class.

        Arguments:
            key {string} -- The key of the driver for the guard to get.

        Returns:
            masonite.drivers.auth.* -- An auth driver class.
        """
        return self._guard.make(key)

    def register_guard(self, key, cls=None):
        """Registers a new guard class.

        Arguments:
            key {string|dict} -- The key to name the guard to a dictionary of key: values

        Keyword Arguments:
            cls {object} -- A guard class. (default: {None})

        Returns:
            None
        """
        if isinstance(key, dict):
            return self.guards.update(key)

        return self.guards.update({key: cls})

    def login(self, *args, **kwargs):
        """Wrapper method to call the guard class method.

        Returns:
            * -- Returns what the guard class method returns.
        """
        return self._guard.login(*args, **kwargs)

    def user(self, *args, **kwargs):
        """Wrapper method to call the guard class method.

        Returns:
            * -- Returns what the guard class method returns.
        """
        return self._guard.user(*args, **kwargs)

    def register(self, *args, **kwargs):
        """Wrapper method to call the guard class method.

        Returns:
            * -- Returns what the guard class method returns.
        """
        return self._guard.register(*args, **kwargs)

    def __getattr__(self, key, *args, **kwargs):
        """Wrapper method to call the guard class methods.

        Returns:
            * -- Returns what the guard class methods returns.
        """
        return getattr(self._guard, key)
