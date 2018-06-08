import os

from masonite.contracts.UploadContract import UploadContract
from masonite.drivers.BaseUploadDriver import BaseUploadDriver


class UploadDiskDriver(BaseUploadDriver, UploadContract):
    """
    Upload from the disk driver
    """

    file_location = None

    def __init__(self, StorageConfig, Application):
        self.config = StorageConfig
        self.appconfig = Application
    
    
    def store(self, fileitem, location=None):
        filename = os.path.basename(fileitem.filename)

        # Check if is a valid extension
        self.validate_extension(filename)

        location = self.get_location(location)
        if not location.endswith('/'):
            location += '/'

        open(location + filename, 'wb').write(fileitem.file.read())

        self.file_location = location + filename

        return filename

    def store_prepend(self, fileitem, prepend, location=None):
        filename = os.path.basename(fileitem.filename)

        location = self.get_location(location)

        open(location + prepend + filename, 'wb').write(fileitem.file.read())

        return prepend + filename
