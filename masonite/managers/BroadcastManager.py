"""Broadcast Manager Module."""

from masonite.contracts import BroadcastManagerContract
from masonite.managers import Manager


class BroadcastManager(Manager, BroadcastManagerContract):
    """Manages all broadcast drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'BroadcastConfig'
    driver_prefix = 'Broadcast'


class Broadcast:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
