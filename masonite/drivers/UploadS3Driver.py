"""Upload S3 Driver."""

import os

from masonite.contracts import UploadContract
from masonite.drivers import BaseUploadDriver
from masonite.exceptions import DriverLibraryNotFound
from masonite.managers import UploadManager
from masonite.app import App


class UploadS3Driver(BaseUploadDriver, UploadContract):
    """Amazon S3 Upload driver."""

    def __init__(self, upload: UploadManager, app: App):
        """Upload Disk Driver Constructor.

        Arguments:
            UploadManager {masonite.managers.UploadManager} -- The Upload Manager object.
            StorageConfig {config.storage} -- Storage configuration.
        """
        self.upload = upload
        self.config = app.make('StorageConfig')

    def store(self, fileitem, filename=None, location=None):
        """Store the file into Amazon S3 server.

        Arguments:
            fileitem {cgi.Storage} -- Storage object.

        Keyword Arguments:
            location {string} -- The location on disk you would like to store the file. (default: {None})
            filename {string} -- A new file name you would like to name the file. (default: {None})

        Raises:
            DriverLibraryNotFound -- Raises when the boto3 library is not installed.

        Returns:
            string -- Returns the file name just saved.
        """
        try:
            import boto3
        except ImportError:
            raise DriverLibraryNotFound(
                'Could not find the "boto3" library. Please pip install this library by running "pip install boto3"')

        driver = self.upload.driver('disk')
        driver.accept_file_types = self.accept_file_types
        driver.store(fileitem, filename=filename, location='storage/temp')
        file_location = driver.file_location

        # use the new filename or get it from the fileitem
        if filename is None:
            filename = self.get_name(fileitem)

        # Check if is a valid extension
        self.validate_extension(filename)

        session = boto3.Session(
            aws_access_key_id=self.config.DRIVERS['s3']['client'],
            aws_secret_access_key=self.config.DRIVERS['s3']['secret'],
        )

        s3 = session.resource('s3')

        if location:
            location = os.path.join(location, filename)
        else:
            location = os.path.join(filename)

        s3.meta.client.upload_file(
            file_location,
            self.config.DRIVERS['s3']['bucket'],
            location
        )

        return filename
