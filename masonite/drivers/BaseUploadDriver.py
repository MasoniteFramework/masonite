from masonite.exceptions import FileTypeException
from masonite.drivers.BaseDriver import BaseDriver


class BaseUploadDriver(BaseDriver):
    """
    Class base for upload drivers
    """

    # this will accept all file types
    accept_file_types = None

    def accept(self, *args, **kwargs):
        """
        Set file types to accept
        """

        self.accept_file_types = args
        return self

    def validate_extension(self, filename):
        """
        Check if files is a valid extension
        """

        if self.accept_file_types is not None:
            if not filename.endswith(self.accept_file_types):
                raise FileTypeException("The extension file not is valid.")

    def get_location(self, location=None):
        if not location:
            location = self.config.DRIVERS['disk']['location']

        if '.' in location:
            location = location.split('.')
            return self.config.DRIVERS[location[0]]['location'][location[1]]
        elif isinstance(location, str):
            return location
        elif isinstance(location, dict):
            return list(location.values())[0]
        
        return location
