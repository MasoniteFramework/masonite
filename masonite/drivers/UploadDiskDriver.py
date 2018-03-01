import os

from masonite.contracts.UploadContract import UploadContract
from masonite.drivers.BaseUploadDriver import BaseUploadDriver


class UploadDiskDriver(BaseUploadDriver, UploadContract):
    """
    Upload from the disk driver
    """

    def __init__(self, StorageConfig, Application):
        self.config = StorageConfig
        self.appconfig = Application

    def store(self, fileitem, location=None):
        filename = os.path.basename(fileitem.filename)

        # Check if is a valid extension
        self.validate_extension(filename)

        if not location:
            location = self.config.DRIVERS['disk']['location']

        location += '/'

        open(location + filename, 'wb').write(fileitem.file.read())

        return location + filename

    def store_prepend(self, fileitem, prepend, location=None):
        filename = os.path.basename(fileitem.filename)

        if not location:
            location = self.config.DRIVERS['disk']['location']

        open(location + prepend + filename, 'wb').write(fileitem.file.read())

        return location + prepend + filename
