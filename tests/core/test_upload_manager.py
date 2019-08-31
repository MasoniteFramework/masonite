import os
import shutil
import unittest

from config import application, storage
from masonite.app import App
from masonite.drivers import UploadDiskDriver, UploadS3Driver
from masonite.environment import LoadEnvironment
from masonite.exceptions import (DriverNotFound, FileTypeException,
                                 UnacceptableDriverType)
from masonite.helpers import static
from masonite.managers.UploadManager import UploadManager

LoadEnvironment()


class TestStaticTemplateHelper(unittest.TestCase):

    def setUp(self):
        self.static = static

    def test_static_gets_first_value_from_dictionary(self):
        self.assertEqual(self.static('disk', 'profile.py'), 'uploads/profile.py')

    def test_static_gets_alias_with_dot_notation(self):
        self.assertEqual(self.static('disk.uploading', 'profile.py'), 'uploads/profile.py')

    def test_static_gets_string_location(self):
        self.assertEqual(self.static('s3', 'profile.py'), 'http://s3.amazon.com/bucket/profile.py')


class TestUploadManager(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Container', self.app)
        self.app.bind('Test', object)
        # self.app.bind('StorageConfig', storage)
        self.app.bind('UploadDiskDriver', UploadDiskDriver)
        self.app.bind('UploadS3Driver', UploadS3Driver)
        self.app.bind('Application', application)
        self.app.bind('UploadManager', UploadManager)

    def test_upload_manager_grabs_drivers(self):
        self.assertIsInstance(self.app.make('UploadManager').driver('disk'), UploadDiskDriver)

    def test_upload_manager_grabs_drivers_with_a_class(self):
        self.assertIsInstance(self.app.make('UploadManager').driver(UploadDiskDriver), UploadDiskDriver)

    def test_upload_manager_throws_error_with_incorrect_file_type(self):
        with self.assertRaises(UnacceptableDriverType):
            self.app.make('UploadManager').driver(static)

    def test_disk_driver_creates_directory_if_not_exists(self):
        print(self.app.make('UploadManager'))
        self.app.make('UploadManager').driver('disk').store(ImageMock(), location="storage/temp")
        self.assertTrue(os.path.exists('storage/temp'))
        shutil.rmtree('storage/temp')

    def test_upload_manager_changes_accepted_files(self):
        self.assertEqual(self.app.make('UploadManager').driver('disk').accept('yml').accept_file_types, ('yml',))
        self.assertEqual(self.app.make('UploadManager').driver('s3').accept('yml').accept_file_types, ('yml',))

    def test_upload_manager_raises_driver_not_found_error(self):
        self.app = App()
        self.app.bind('Test', object)
        # self.app.bind('StorageConfig', storage)

        with self.assertRaises(DriverNotFound):
            self.assertIsNone(self.app.bind(
                'UploadManager',
                UploadManager(self.app).load_container(self.app)
            ))

    def test_upload_manager_switches_drivers(self):
        self.app.bind('UploadTestDriver', UploadDiskDriver)

        self.assertIsInstance(self.app.make(
            'UploadManager').driver('disk'), UploadDiskDriver)

        self.assertIsInstance(self.app.make('UploadManager').driver('test'), UploadDiskDriver)

    def test_upload_file(self):
        """
        This test is responsible for checking if you upload a file correctly.
        """

        self.assertTrue(UploadManager(self.app).driver('disk').store(ImageMock()))

    def test_upload_file_with_location(self):
        """
        This test is responsible for checking if you upload a file correctly.
        """

        self.assertTrue(UploadManager(self.app).driver('disk').store(ImageMock(), location='uploads'))

    def test_upload_file_with_location_from_driver(self):
        """
        This test is responsible for checking if you upload a file correctly.
        """

        self.assertTrue(UploadManager(self.app).driver('disk').store(ImageMock(), location='disk.uploading'))

    def test_upload_manage_accept_files(self):
        """
        This test is responsible for checking if you upload
        a file correctly with a valid extension.
        """
        self.assertTrue(UploadManager(self.app).driver('disk').accept('jpg', 'png').store(ImageMock()))

    def test_upload_manage_accept_files_error(self):
        """
        This test should return an error because it is an invalid extension.
        """
        with self.assertRaises(FileTypeException):
            UploadManager(self.app).driver('disk').accept('png').store(ImageMock())

    def test_upload_manage_accept_all_extensions(self):
        """
        This test should upload a file correctly by allowing all type files ( .accept('*') )
        """

        image = ImageMock()
        image.filename = 'file.pdf'

        print(image.filename)

        self.assertTrue(UploadManager(self.app).driver('disk').accept('*').store(image))

    def test_upload_manage_should_raise_exception_when_accept_all_extension_and_something_more(self):
        """
        This test should raise an error when use something together with '*' when allowing all extensions )
        """
        with self.assertRaises(ValueError):
            UploadManager(self.app).driver('disk').accept('*', 'png').store(ImageMock())

    def test_upload_with_new_filename(self):
        self.assertEqual(self.app.make('UploadManager').driver('disk').store(ImageMock(), filename='newname.jpg'), 'newname.jpg')

    def test_upload_manager_validates_file_ext(self):
        """
        This test is responsible for checking if you upload
        a file correctly with a valid extension.
        """
        self.assertTrue(UploadManager(self.app).driver('disk').accept('jpg', 'png').validate_extension('test.png'))


class ImageMock:
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

    class TestS3Upload(unittest.TestCase):

        def setUp(self):
            self.app = App()
            self.app.bind('Container', self.app)

            self.app.bind('Application', application)
            # self.app.bind('StorageConfig', storage)
            self.app.bind('UploadDiskDriver', UploadDiskDriver)
            self.app.bind('UploadManager', UploadManager(self.app))
            self.app.bind('Upload', UploadManager(self.app))
            self.app.bind('UploadS3Driver', UploadS3Driver)

        def test_upload_file_for_s3(self):
            self.assertEqual(len(self.app.make('Upload').driver('s3').store(ImageMock())), 29)

        def test_upload_open_file_for_s3(self):
            self.assertTrue(self.app.make('Upload').driver('s3').accept('yml').store(open('.travis.yml')))

        def test_upload_manage_accept_files(self):
            """
            This test is responsible for checking if you upload
            a file correctly with a valid extension.
            """
            self.assertTrue(UploadManager(self.app).driver('s3').accept('jpg', 'png').store(ImageMock()))

        def test_upload_manage_accept_files_error(self):
            """
            This test should return an error because it is an invalid extension.
            """
            with self.assertRaises(FileTypeException):
                UploadManager(self.app).driver('s3').accept('png').store(ImageMock())

        def test_upload_with_new_filename(self):
            self.assertEqual(self.app.make('UploadManager').driver('s3').store(ImageMock(), filename='newname.jpg'), 'newname.jpg')

        def test_upload_with_new_filename_and_location_in_s3(self):
            self.assertEqual(self.app.make('UploadManager').driver('s3').store(ImageMock(), filename='newname.jpg', location='3/2'), 'newname.jpg')
