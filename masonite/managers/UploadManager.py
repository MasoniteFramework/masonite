""" Upload Manager Module """

from masonite.managers.Manager import Manager


class UploadManager(Manager):
    """Manages all upload drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'StorageConfig'
    driver_prefix = 'Upload'
