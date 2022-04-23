from tests import TestCase


class TestResponseDownload(TestCase):
    def setUp(self):
        super().setUp()
        self.response = self.make_response()

    def test_download(self):
        self.response.download(
            "invoice", "tests/integrations/storage/invoice.pdf", force=True
        )
        self.assertTrue(self.response.header("Content-Disposition"))
        self.assertEqual(
            self.response.header("Content-Disposition"),
            'attachment; filename="invoice.pdf"',
        )
