from src.masonite.testing import TestCase
from src.masonite.response import Download
from src.masonite.routes import Get

class DownloadTestController:

    def show(self):
        return Download('uploads/profile.jpg')

    def force(self):
        return Download('uploads/profile.jpg', name="me.jpg").force()

class TestDownload(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(only=[
            Get('/download', DownloadTestController.show),
            Get('/download/force', DownloadTestController.force),
        ])

    def test_can_show_download(self):
        (self.get('/download')
            .assertIsStatus(200)
            .assertHeaderIs('Content-Type', 'image/jpeg')
            .assertHasHeader('Content-Type')
            .assertNotHasHeader('Content-Disposition')
        )

    def test_can_download_file(self):
        (self.get('/download/force')
            .assertIsStatus(200)
            .assertHeaderIs('Content-Type', 'application/octet-stream')
            .assertHeaderIs('Content-Disposition', 'attachment; filename="{}"'.format('me.jpg'))
        )
