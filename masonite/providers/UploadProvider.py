""" An Upload Service Provider """
from masonite.provider import ServiceProvider
from masonite.managers.UploadManager import UploadManager
from masonite.drivers.UploadDiskDriver import UploadDiskDriver
from masonite.drivers.UploadS3Driver import UploadS3Driver
from config import storage
from masonite.helpers.static import static


class UploadProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('StorageConfig', storage)
        self.app.bind('UploadDiskDriver', UploadDiskDriver)
        self.app.bind('UploadS3Driver', UploadS3Driver)
        self.app.bind('UploadManager', UploadManager(self.app))

    def boot(self, UploadManager, StorageConfig, ViewClass):
        self.app.bind('Upload', UploadManager.driver(StorageConfig.DRIVER))
        ViewClass.share(
            {
                'static': static,
            }
        )
