"""Queue Manager Module."""

from ..contracts import StorageManagerContract
from .Manager import Manager


class StorageManager(Manager, StorageManagerContract):
    """Manages all queue drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'storage'
    driver_prefix = 'Storage'


class Storage:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
