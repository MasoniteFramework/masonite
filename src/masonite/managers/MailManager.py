"""Mail Manager Module."""

from ..contracts import MailManagerContract
from .Manager import Manager
from ..helpers import config


class MailManager(Manager, MailManagerContract):
    """Manages all mail drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'mail'
    driver_prefix = 'Mail'

    def helper(self):
        """Helper Method to work with returning the driver from the MailManager.

        Returns:
            Mail Driver
        """
        return self.driver(config('mail.driver'))


class Mail:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
