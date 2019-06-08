"""Base upload driver module."""

import _io
from masonite.drivers import BaseDriver
from masonite.exceptions import FileTypeException
from masonite.helpers import random_string
from masonite.helpers import config


class BaseUploadDriver(BaseDriver):
    """Base class that all upload drivers inherit from."""

    accept_file_types = ('jpg', 'jpeg', 'png', 'gif', 'bmp')

    def accept(self, *args, **kwargs):
        """Set file types to accept before uploading.

        Returns:
            self
        """

        extensions = list(args)

        if '*' in extensions and len(extensions) > 1:
            raise ValueError("When uses '*' isn't allowed accept other file type.")

        if extensions == ['*']:
            self.accept_file_types = None
        else:
            self.accept_file_types = args

        return self

    def validate_extension(self, filename):
        """Check for valid file extenstions set with the 'accept' method.

        Arguments:
            filename {string} -- The filename with file extension to validate.

        Raises:
            FileTypeException -- Thrown if the specified file extension is incorrect.
        """
        if self.accept_file_types is not None:
            if not filename.endswith(self.accept_file_types):
                raise FileTypeException("The file extension is not supported.")

        return True

    def get_location(self, location=None):
        """Get the location of where to upload.

        Keyword Arguments:
            location {string} -- The path to upload to. If none then this will check for configuration settings. (default: {None})

        Returns:
            string -- Returns the location it uploaded to.
        """
        if not location:
            location = config('storage.drivers.disk.location')

        if '.' in location:
            location = location.split('.')
            return config('storage.drivers')[location[0]]['location'][location[1]]
        elif isinstance(location, str):
            return location
        elif isinstance(location, dict):
            return list(location.values())[0]

        return location

    def get_name(self, fileitem):
        return "{}.{}".format(random_string(25).lower(), self.get_extension(fileitem))

    def get_extension(self, fileitem):
        if isinstance(fileitem, _io.TextIOWrapper):
            return fileitem.name.split('.')[-1]
        else:
            return fileitem.filename.split('.')[-1]
