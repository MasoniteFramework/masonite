from config import storage
import pytest

from masonite.app import App
from masonite.exceptions import DriverNotFound
from masonite.managers.UploadManager import UploadManager


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
        container.bind('UploadManager', UploadManager().load_container(container))


def test_upload_manager_switches_drivers():
    container = App()

    container.bind('Test', object)
    container.bind('StorageConfig', storage)
    container.bind('UploadDiskDriver', object)
    container.bind('UploadTestDriver', object)

    container.bind('UploadManager', UploadManager(container).driver('test'))
