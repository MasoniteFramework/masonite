""" An Upload Service Provider """

from config import storage
from masonite.drivers import UploadDiskDriver, UploadS3Driver
from masonite.helpers.static import static
from masonite.managers import UploadManager
from masonite.provider import ServiceProvider


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
