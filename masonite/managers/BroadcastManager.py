""" Broadcast Manager Module """

from masonite.managers import Manager


class BroadcastManager(Manager):
    """Manages all broadcast drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'BroadcastConfig'
    driver_prefix = 'Broadcast'
