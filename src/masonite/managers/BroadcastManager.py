"""Broadcast Manager Module."""

from ..contracts import BroadcastManagerContract
from .Manager import Manager


class BroadcastManager(Manager, BroadcastManagerContract):
    """Manages all broadcast drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'broadcast'
    driver_prefix = 'Broadcast'


class Broadcast:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
