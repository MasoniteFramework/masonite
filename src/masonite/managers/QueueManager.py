"""Queue Manager Module."""

from ..contracts import QueueManagerContract
from .Manager import Manager


class QueueManager(Manager, QueueManagerContract):
    """Manages all queue drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'queue'
    driver_prefix = 'Queue'


class Queue:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
