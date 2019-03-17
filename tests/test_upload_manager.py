import os
import shutil

import pytest

from config import application, storage
from masonite.app import App
from masonite.drivers import UploadDiskDriver, UploadS3Driver
from masonite.environment import LoadEnvironment
from masonite.exceptions import (DriverNotFound, FileTypeException,
                                 UnacceptableDriverType)
from masonite.helpers import static
from masonite.managers.UploadManager import UploadManager

LoadEnvironment()



class TestStaticTemplateHelper:

    def setup_method(self):
        self.static = static

    def test_static_gets_first_value_from_dictionary(self):
        assert self.static('disk', 'profile.py') == 'uploads/profile.py'

    def test_static_gets_alias_with_dot_notation(self):
        assert self.static('disk.uploading', 'profile.py') == 'uploads/profile.py'

    def test_static_gets_string_location(self):
        assert self.static('s3', 'profile.py') == 'http://s3.amazon.com/bucket/profile.py'


class TestUploadManager:

    def setup_method(self):
        self.app = App()
        self.app.bind('Container', self.app)
        self.app.bind('Test', object)
        self.app.bind('StorageConfig', storage)
        self.app.bind('UploadDiskDriver', UploadDiskDriver)
        self.app.bind('UploadS3Driver', UploadS3Driver)
        self.app.bind('Application', application)
        self.app.bind('UploadManager', UploadManager().load_container(self.app))

    def test_upload_manager_grabs_drivers(self):
        assert isinstance(self.app.make('UploadManager').driver('disk'), UploadDiskDriver)

    def test_upload_manager_grabs_drivers_with_a_class(self):
        assert isinstance(self.app.make('UploadManager').driver(UploadDiskDriver), UploadDiskDriver)

    def test_upload_manager_throws_error_with_incorrect_file_type(self):
        with pytest.raises(UnacceptableDriverType):
            self.app.make('UploadManager').driver(static)

    def test_disk_driver_creates_directory_if_not_exists(self):
        self.app.make('UploadManager').driver('disk').store(ImageMock(), location="storage/temp")
        assert os.path.exists('storage/temp')
        shutil.rmtree('storage/temp')

    def test_upload_manager_changes_accepted_files(self):
        assert self.app.make('UploadManager').driver('disk').accept('yml').accept_file_types == ('yml',)
        assert self.app.make('UploadManager').driver('s3').accept('yml').accept_file_types == ('yml',)

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

        assert UploadManager(self.app).driver('disk').store(ImageMock(), location='uploads')

    def test_upload_file_with_location_from_driver(self):
        """
        This test is responsible for checking if you upload a file correctly.
        """

        assert UploadManager(self.app).driver('disk').store(ImageMock(), location='disk.uploading')

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

    def test_upload_with_new_filename(self):
        assert self.app.make('UploadManager').driver('disk').store(ImageMock(), filename='newname.jpg') == 'newname.jpg'

    def test_upload_manager_validates_file_ext(self):
        """
        This test is responsible for checking if you upload
        a file correctly with a valid extension.
        """
        assert UploadManager(self.app).driver('disk').accept('jpg', 'png').validate_extension('test.png')

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
            self.app.bind('Container', self.app)

            self.app.bind('Application', application)
            self.app.bind('StorageConfig', storage)
            self.app.bind('UploadDiskDriver', UploadDiskDriver)
            self.app.bind('UploadManager', UploadManager(self.app))
            self.app.bind('Upload', UploadManager(self.app))
            self.app.bind('UploadS3Driver', UploadS3Driver)

        def test_upload_file_for_s3(self):
            assert len(self.app.make('Upload').driver('s3').store(ImageMock())) == 29

        def test_upload_open_file_for_s3(self):
            assert self.app.make('Upload').driver('s3').accept('yml').store(open('.travis.yml'))

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

        def test_upload_with_new_filename(self):
            assert self.app.make('UploadManager').driver('s3').store(ImageMock(), filename='newname.jpg') == 'newname.jpg'

        def test_upload_with_new_filename_and_location_in_s3(self):
            assert self.app.make('UploadManager').driver('s3').store(ImageMock(), filename='newname.jpg', location='3/2') == 'newname.jpg'
