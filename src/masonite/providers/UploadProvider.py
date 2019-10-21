"""An Upload Service Provider."""

from ..drivers import UploadDiskDriver, UploadS3Driver
from ..helpers.static import static
from ..managers import UploadManager
from ..provider import ServiceProvider
from ..view import View
from .. import Upload
from ..helpers import config


class UploadProvider(ServiceProvider):

    wsgi = False

    def register(self):
        # from config import storage
        # self.app.bind('StorageConfig', storage)
        self.app.bind('UploadDiskDriver', UploadDiskDriver)
        self.app.bind('UploadS3Driver', UploadS3Driver)
        self.app.bind('UploadManager', UploadManager(self.app))

    def boot(self, manager: UploadManager, view: View):
        self.app.bind('Upload', manager.driver(config('storage').DRIVER))
        self.app.swap(Upload, manager.driver(config('storage').DRIVER))
        view.share(
            {
                'static': static,
            }
        )
