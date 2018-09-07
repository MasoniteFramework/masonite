""" Queue Manager Module """

from masonite.contracts import QueueManagerContract
from masonite.managers import Manager


class QueueManager(Manager, QueueManagerContract):
    """Manages all queue drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'QueueConfig'
    driver_prefix = 'Queue'
