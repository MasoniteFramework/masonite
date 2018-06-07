import os
import pytest

from config import application, storage
from masonite.app import App
from masonite.exceptions import DriverNotFound, FileTypeException
from masonite.managers.UploadManager import UploadManager
from masonite.drivers.UploadDiskDriver import UploadDiskDriver
from masonite.drivers.UploadS3Driver import UploadS3Driver


class TestUploadManager:

    def setup_method(self):
        self.app = App()
        self.app.bind('Test', object)
        self.app.bind('StorageConfig', storage)
        self.app.bind('UploadDiskDriver', UploadDiskDriver)
        self.app.bind('Application', application)
        self.app.bind('UploadManager', UploadManager().load_container(self.app))

    def test_upload_manager_grabs_drivers(self):
        assert isinstance(self.app.make('UploadManager').driver('disk'), UploadDiskDriver)

    def test_upload_manager_raises_driver_not_found_error(self):
        self.app = App()
        self.app.bind('Test', object)
        self.app.bind('StorageConfig', storage)

        with pytest.raises(DriverNotFound):
            assert self.app.bind(
                'UploadManager',
                UploadManager().load_container(self.app)
            )

    def test_upload_manager_switches_drivers(self):
        self.app.bind('UploadTestDriver', UploadDiskDriver)

        assert isinstance(self.app.make(
            'UploadManager').driver('disk'), UploadDiskDriver)
        
        assert isinstance(self.app.make('UploadManager').driver('test'), UploadDiskDriver)

    def test_upload_file(self):
        """
        This test is responsible for checking if you upload a file correctly.
        """

        assert UploadManager(self.app).driver('disk').store(ImageMock())
    
    def test_upload_file_with_location(self):
        """
        This test is responsible for checking if you upload a file correctly.
        """

        assert UploadManager(self.app).driver('disk').store(ImageMock(), 'uploads')

    def test_upload_file_with_location_from_driver(self):
        """
        This test is responsible for checking if you upload a file correctly.
        """

        assert UploadManager(self.app).driver('disk').store(ImageMock(), 'disk.uploading')

    def test_upload_manage_accept_files(self):
        """
        This test is responsible for checking if you upload
        a file correctly with a valid extension.
        """
        assert UploadManager(self.app).driver('disk').accept('jpg', 'png').store(ImageMock())

    def test_upload_manage_accept_files_error(self):
        """
        This test should return an error because it is an invalid extension.
        """
        with pytest.raises(FileTypeException):
            UploadManager(self.app).driver('disk').accept('png').store(ImageMock())


class ImageMock():
    """
    Image test for emulate upload file
    """

    filename = 'test.jpg'

    @property
    def file(self):
        return self
    
    def read(self):
        return bytes('file read', 'utf-8')



if os.environ.get('S3_BUCKET'):

    class TestS3Upload:

        def setup_method(self):
            self.app = App()

            self.app.bind('Application', application)
            self.app.bind('StorageConfig', storage)
            self.app.bind('UploadDiskDriver', UploadDiskDriver)
            self.app.bind('UploadManager', UploadManager(self.app))
            self.app.bind('Upload', UploadManager(self.app))
            self.app.bind('UploadS3Driver', UploadS3Driver)

        def test_upload_file_for_s3(self):
            assert self.app.make('Upload').driver('s3').store(ImageMock()) == 'test.jpg'


        def test_upload_manage_accept_files(self):
            """
            This test is responsible for checking if you upload
            a file correctly with a valid extension.
            """
            assert UploadManager(self.app).driver('s3').accept('jpg', 'png').store(ImageMock())


        def test_upload_manage_accept_files_error(self):
            """
            This test should return an error because it is an invalid extension.
            """
            with pytest.raises(FileTypeException):
                UploadManager(self.app).driver('s3').accept('png').store(ImageMock())

        def test_upload_store_prepend(self):
            assert self.app.make('UploadManager').driver('s3').store_prepend(ImageMock(), 'hey') == 'heytest.jpg'
