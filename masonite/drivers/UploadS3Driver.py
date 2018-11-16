""" Upload S3 Driver """

from masonite.contracts.UploadContract import UploadContract
from masonite.drivers.BaseUploadDriver import BaseUploadDriver
from masonite.exceptions import DriverLibraryNotFound


class UploadS3Driver(BaseUploadDriver, UploadContract):
    """
    Amazon S3 Upload driver
    """

    def __init__(self, UploadManager, StorageConfig):
        """Upload Disk Driver Constructor

        Arguments:
            UploadManager {masonite.managers.UploadManager} -- The Upload Manager object.
            StorageConfig {config.storage} -- Storage configuration.
        """

        self.upload = UploadManager
        self.config = StorageConfig

    def store(self, fileitem, location=None):
        """Store the file into Amazon S3 server.

        Arguments:
            fileitem {cgi.Storage} -- Storage object.

        Keyword Arguments:
            location {string} -- The location on disk you would like to store the file. (default: {None})

        Raises:
            DriverLibraryNotFound -- Raises when the boto3 library is not installed.

        Returns:
            string -- Returns the file name just saved.
        """

        driver = self.upload.driver('disk')
        driver.store(fileitem, location)
        file_location = driver.file_location

        filename = self.get_name(fileitem)

        # Check if is a valid extension
        self.validate_extension(filename)

        try:
            import boto3
        except ImportError:
            raise DriverLibraryNotFound(
                'Could not find the "boto3" library. Please pip install this library by running "pip install boto3"')

        session = boto3.Session(
            aws_access_key_id=self.config.DRIVERS['s3']['client'],
            aws_secret_access_key=self.config.DRIVERS['s3']['secret'],
        )

        s3 = session.resource('s3')

        s3.meta.client.upload_file(
            file_location,
            self.config.DRIVERS['s3']['bucket'],
            filename
        )

        return filename

    def store_prepend(self, fileitem, prepend, location=None):
        """Store the file onto the Amazon S3 server but with a prepended file name.

        Arguments:
            fileitem {cgi.Storage} -- Storage object.
            prepend {string} -- The prefix you want to prepend to the file name.

        Keyword Arguments:
            location {string} -- The location on disk you would like to store the file. (default: {None})

        Returns:
            string -- Returns the file name just saved.
        """

        fileitem.filename = prepend + fileitem.filename

        return self.store(fileitem, location=location)
