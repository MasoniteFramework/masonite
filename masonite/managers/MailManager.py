""" Mail Manager Module """

from masonite.managers.Manager import Manager


class MailManager(Manager):
    """Manages all mail drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'MailConfig'
    driver_prefix = 'Mail'
