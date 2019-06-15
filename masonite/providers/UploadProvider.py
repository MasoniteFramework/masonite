"""An Upload Service Provider."""

from masonite.drivers import UploadDiskDriver, UploadS3Driver
from masonite.helpers.static import static
from masonite.managers import UploadManager
from masonite.provider import ServiceProvider
from masonite.view import View
from masonite import Upload


class UploadProvider(ServiceProvider):

    wsgi = False

    def register(self):
        from config import storage
        self.app.bind('StorageConfig', storage)
        self.app.bind('UploadDiskDriver', UploadDiskDriver)
        self.app.bind('UploadS3Driver', UploadS3Driver)
        self.app.bind('UploadManager', UploadManager(self.app))

    def boot(self, manager: UploadManager, view: View):
        self.app.bind('Upload', manager.driver(self.app.make('StorageConfig').DRIVER))
        self.app.swap(Upload, manager.driver(self.app.make('StorageConfig').DRIVER))
        view.share(
            {
                'static': static,
            }
        )
