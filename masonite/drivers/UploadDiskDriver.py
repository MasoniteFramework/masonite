""" Upload Disk Driver """

import os
import _io

from masonite.contracts.UploadContract import UploadContract
from masonite.drivers.BaseUploadDriver import BaseUploadDriver


class UploadDiskDriver(BaseUploadDriver, UploadContract):
    """Upload to and from the file system.
    """

    file_location = None

    def __init__(self, StorageConfig, Application):
        """Upload Disk Driver Constructor

        Arguments:
            StorageConfig {config.storage} -- Storage configuration.
            Application {masonite.app.App} -- The application container.
        """

        self.config = StorageConfig
        self.appconfig = Application

    def store(self, fileitem, location=None):
        """Store the file onto a server.

        Arguments:
            fileitem {cgi.Storage} -- Storage object.

        Keyword Arguments:
            location {string} -- The location on disk you would like to store the file. (default: {None})

        Returns:
            string -- Returns the file name just saved.
        """

        filename = self.get_name(fileitem)

        # Check if is a valid extension
        self.validate_extension(filename)

        location = self.get_location(location)
        if not location.endswith('/'):
            location += '/'

        if isinstance(fileitem, _io.TextIOWrapper):
            open(location + filename, 'wb').write(bytes(fileitem.read(), 'utf-8'))
        else:
            open(location + filename, 'wb').write(fileitem.file.read())

        self.file_location = location + filename

        return filename

    def store_prepend(self, fileitem, prepend, location=None):
        """Store the file onto a server but with a prepended file name.

        Arguments:
            fileitem {cgi.Storage} -- Storage object.
            prepend {string} -- The prefix you want to prepend to the file name.

        Keyword Arguments:
            location {string} -- The location on disk you would like to store the file. (default: {None})

        Returns:
            string -- Returns the file name just saved.
        """

        filename = os.path.basename(fileitem.filename)

        location = self.get_location(location)

        open(location + prepend + filename, 'wb').write(fileitem.file.read())

        return prepend + filename
