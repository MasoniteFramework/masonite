"""Queue Manager Module."""

from masonite.contracts import StorageManagerContract
from masonite.managers import Manager


class StorageManager(Manager, StorageManagerContract):
    """Manages all queue drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'StorageConfig'
    driver_prefix = 'Storage'


class Storage:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
