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
