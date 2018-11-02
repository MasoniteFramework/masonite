"""Mail Manager Module."""

from masonite.contracts import MailManagerContract
from masonite.managers import Manager


class MailManager(Manager, MailManagerContract):
    """Manages all mail drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'MailConfig'
    driver_prefix = 'Mail'

    def helper(self):
        """Helper Method to work with returning the driver from the MailManager.

        Returns:
            Mail Driver
        """
        return self.driver(self.container.make('MailConfig').DRIVER)


class Mail:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
