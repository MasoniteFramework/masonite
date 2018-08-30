""" Queue Manager Module """

from masonite.managers.Manager import Manager


class QueueManager(Manager):
    """Manages all queue drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'QueueConfig'
    driver_prefix = 'Queue'
