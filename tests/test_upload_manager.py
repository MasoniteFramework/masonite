import os
import pytest

from config import application, storage
from masonite.app import App
from masonite.exceptions import DriverNotFound, FileTypeException
from masonite.managers.UploadManager import UploadManager
from masonite.drivers.UploadDiskDriver import UploadDiskDriver
from masonite.drivers.UploadS3Driver import UploadS3Driver


def test_upload_manager_grabs_drivers():
    container = App()

    container.bind('Test', object)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', UploadDiskDriver)
    container.bind('Application', application)
    container.bind('UploadManager', UploadManager().load_container(container))

    assert isinstance(container.make('UploadManager').driver('disk'), UploadDiskDriver)

def test_upload_manager_raises_driver_not_found_error():
    container = App()

    container.bind('Test', object)
    container.bind('StorageConfig', storage)

    with pytest.raises(DriverNotFound):
        assert container.bind(
            'UploadManager',
            UploadManager().load_container(container)
        )


def test_upload_manager_switches_drivers():
    container = App()

    container.bind('Test', object)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', UploadDiskDriver)
    container.bind('UploadTestDriver', object)
    container.bind('Application', application)
    container.bind('UploadManager', UploadManager(container))

    assert isinstance(container.make(
        'UploadManager').driver('disk'), UploadDiskDriver)
    
    assert isinstance(container.make('UploadManager').driver('test'), object)

class ImageTest():
    """
    Image test for emulate upload file
    """

    @property
    def filename(self):
        return os.getcwd() + "/tests/static/test.jpg"

    @property
    def file(self):
        return open(self.filename, 'rb')


def test_upload_file():
    """
    This test is responsible for checking if you upload a file correctly.
    """

    container = App()

    container.bind('Application', application)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', UploadDiskDriver)
    container.bind('UploadManager', UploadManager(container))
    container.bind('Upload', UploadManager(container))
    container.bind('UploadS3Driver', UploadS3Driver)

    img = ImageTest()

    assert UploadManager(container).driver('disk').store(img)

if os.environ.get('S3_BUCKET'):
    def test_upload_file_for_s3():

        container = App()

        container.bind('Application', application)
        container.bind('StorageConfig', storage)
        container.bind('UploadDiskDriver', UploadDiskDriver)
        container.bind('UploadManager', UploadManager(container))
        container.bind('Upload', UploadManager(container))
        container.bind('UploadS3Driver', UploadS3Driver)

        img = ImageTest()

        assert container.make('Upload').driver('s3').store(img) is None


def test_upload_manage_accept_files():
    """
    This test is responsible for checking if you upload
    a file correctly with a valid extension.
    """

    container = App()

    container.bind('Application', application)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', UploadDiskDriver)

    img = ImageTest()
    assert UploadManager(container).driver('disk').accept('jpg', 'png').store(img)


def test_upload_manage_accept_files_error():
    """
    This test should return an error because it is an invalid extension.
    """

    container = App()

    container.bind('Application', application)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', UploadDiskDriver)

    img = ImageTest()
    with pytest.raises(FileTypeException):
        UploadManager(container).driver('disk').accept('png').store(img)

def test_upload_store_prepend():
    container = App()

    container.bind('Application', application)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', UploadDiskDriver)
    container.bind('UploadManager', UploadManager(container))

    assert container.make('UploadManager').driver('disk').store_prepend(ImageTest(), 'hey') == 'uploads/heytest.jpg'
