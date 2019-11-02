
class AuthenticationGuard:

    def guard(self, guard):
        """Specify the guard you want to use

        Arguments:
            guard {[type]} -- [description]
        """
        from .Guard import Guard
        return Guard(self.app).make(guard)

    def register_guard(self, key, cls=None):
        """Registers a new guard class.

        Arguments:
            key {string|dict} -- The key to name the guard to a dictionary of key: values

        Keyword Arguments:
            cls {object} -- A guard class. (default: {None})

        Returns:
            None
        """
        from .Guard import Guard
        if isinstance(key, dict):
            return Guard.guards.update(key)

        return Guard.guards.update({key: cls})

    def register_driver(self, key, cls):
        """Registers a new driver with the current guard class.

        Arguments:
            key {string} -- The key to register the driver to.
            cls {class} -- A guard class.
        """
        self.drivers.update({key: cls})

    def make(self, key):
        """Makes a new driver from the current guard class.

        Arguments:
            key {string} -- The key to for the driver to make.

        Raises:
            DriverNotFound: Thrown when the driver is not registered.

        Returns:
            object -- Returns a guard driver object.
        """
        if key in self.drivers:
            self.driver = self.app.resolve(self.drivers[key])
            return self.driver

        raise DriverNotFound("Could not find the driver {}".format(key))
