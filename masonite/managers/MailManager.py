""" Mail Manager Module """

from masonite.managers.Manager import Manager


class MailManager(Manager):
    """Manages all mail drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'MailConfig'
    driver_prefix = 'Mail'

    def helper(self):
        """Helper Method to work with returning the driver from the MailManager
        
        Returns:
            Mail Driver
        """
        return self.driver(self.container.make('MailConfig').DRIVER)
