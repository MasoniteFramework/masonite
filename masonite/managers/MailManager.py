""" Mail Manager Module """

from masonite.contracts import MailManagerContract
from masonite.managers import Manager


class MailManager(Manager, MailManagerContract):
    """Manages all mail drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'MailConfig'
    driver_prefix = 'Mail'
