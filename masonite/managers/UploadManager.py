from masonite.managers.Manager import Manager


class UploadManager(Manager):
    """
    Upload files manager class
    """

    config = 'StorageConfig'
    driver_prefix = 'Upload'
