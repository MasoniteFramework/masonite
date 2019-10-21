"""Upload Manager Module."""

from ..contracts import UploadManagerContract
from .Manager import Manager


class UploadManager(Manager, UploadManagerContract):
    """Manages all upload drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'storage'
    driver_prefix = 'Upload'


class Upload:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
