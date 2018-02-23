import os
import pytest

from config import application, storage
from masonite.app import App
from masonite.exceptions import DriverNotFound, FileTypeException
from masonite.managers.UploadManager import UploadManager
from masonite.drivers.UploadDiskDriver import UploadDiskDriver


def test_upload_manager_grabs_drivers():
    container = App()

    container.bind('Test', object)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', object)
    container.bind('UploadManager', UploadManager().load_container(container))


def test_upload_manager_raises_driver_not_found_error():
    container = App()

    container.bind('Test', object)
    container.bind('StorageConfig', storage)

    with pytest.raises(DriverNotFound):
        container.bind(
            'UploadManager',
            UploadManager().load_container(container)
        )


def test_upload_manager_switches_drivers():
    container = App()

    container.bind('Test', object)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', object)
    container.bind('UploadTestDriver', object)
    container.bind('UploadManager', UploadManager(container).driver('test'))


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

    img = ImageTest()
    assert UploadManager(container).driver('disk').store(img)


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
    try:
        UploadManager(container).driver('disk').accept('png').store(img)
        assert False
    except FileTypeException:
        assert True
