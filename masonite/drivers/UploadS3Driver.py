
from masonite.contracts.UploadContract import UploadContract
from masonite.drivers.BaseUploadDriver import BaseUploadDriver
from masonite.exceptions import DriverLibraryNotFound


class UploadS3Driver(BaseUploadDriver, UploadContract):
    """
    Amazon S3 Upload driver
    """

    def __init__(self, UploadManager, StorageConfig):
        self.upload = UploadManager
        self.config = StorageConfig

    def store(self, fileitem, location=None):
        driver = self.upload.driver('disk')
        driver.store(fileitem, location)
        file_location = driver.file_location

        # Check if is a valid extension
        self.validate_extension(fileitem.filename)

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
            fileitem.filename
        )

        return fileitem.filename

    def store_prepend(self, fileitem, prepend, location=None):
        fileitem.filename = prepend + fileitem.filename

        return self.store(fileitem, location=location)
