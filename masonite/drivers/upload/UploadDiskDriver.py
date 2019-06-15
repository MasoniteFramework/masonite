"""Upload Disk Driver."""

import os
import _io

from masonite.contracts import UploadContract
from masonite.drivers import BaseUploadDriver
from masonite.helpers.filesystem import make_directory


class UploadDiskDriver(BaseUploadDriver, UploadContract):
    """Upload to and from the file system."""

    file_location = None

    def __init__(self):
        """Upload Disk Driver Constructor."""
        pass

    def store(self, fileitem, filename=None, location=None):
        """Store the file onto a server.

        Arguments:
            fileitem {cgi.Storage} -- Storage object.

        Keyword Arguments:
            location {string} -- The location on disk you would like to store the file. (default: {None})
            filename {string} -- A new file name you would like to name the file. (default: {None})

        Returns:
            string -- Returns the file name just saved.
        """

        # use the new filename or get it from the fileitem
        if filename is None:
            filename = self.get_name(fileitem)

        # Check if is a valid extension
        self.validate_extension(self.get_name(fileitem))

        location = self.get_location(location)

        location = os.path.join(location, filename)

        make_directory(location)

        if isinstance(fileitem, _io.TextIOWrapper):
            with open(location, 'wb') as file:
                file.write(bytes(fileitem.read(), 'utf-8'))
        else:
            with open(location, 'wb') as file:
                file.write(fileitem.file.read())

        self.file_location = location

        return filename
