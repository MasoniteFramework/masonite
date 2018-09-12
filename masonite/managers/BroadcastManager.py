""" Broadcast Manager Module """

from masonite.contracts import BroadcastManagerContract
from masonite.managers import Manager


class BroadcastManager(Manager, BroadcastManagerContract):
    """Manages all broadcast drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'BroadcastConfig'
    driver_prefix = 'Broadcast'
