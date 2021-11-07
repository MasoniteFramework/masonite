from tests import TestCase
from src.masonite.foundation import Application
import os
from src.masonite.response import Response


class TestResponseRedirect(TestCase):
    def setUp(self):
        application = Application(os.getcwd())
        self.response = Response(application)

    def test_download(self):
        self.response.download(
            "invoice", "tests/integrations/storage/invoice.pdf", force=True
        )
        self.assertTrue(self.response.header("Content-Disposition"))
        self.assertEqual(
            self.response.header("Content-Disposition"),
            'attachment; filename="invoice.pdf"',
        )
