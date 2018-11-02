"""The base class that all drivers inherit from."""


class BaseDriver:
    """Base driver class."""

    _manager = None

    def driver(self, driver):
        """Return an instance of the driver specified.

        Arguments:
            driver {string} -- String representation of the driver to be resolved from the container.
                               This can be values like "s3" or "disk"

        Returns:
            masonite.drivers -- Returns an instance of the driver.
        """
        return self._manager.driver(driver)

    def load_manager(self, manager):
        """Load the manager into the driver.

        Arguments:
            manager {masonite.managers} -- Needs to be a Manager class.

        Returns:
            self
        """
        self._manager = manager
        return self
