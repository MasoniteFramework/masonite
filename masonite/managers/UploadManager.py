"""Upload Manager Module."""

from masonite.contracts import UploadManagerContract
from masonite.managers import Manager


class UploadManager(Manager, UploadManagerContract):
    """Manages all upload drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'StorageConfig'
    driver_prefix = 'Upload'


class Upload:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
