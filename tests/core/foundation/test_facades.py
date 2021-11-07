from tests import TestCase
from src.masonite.facades import Mail, View


class TestFacades(TestCase):
    def test_mail_facade(self):
        self.assertIsNone(Mail.get_config_options("mailgun")["domain"])

    def test_view_facade(self):
        View.add_location("tests/integrations/templates")
        self.assertEqual("test", View.render("test", {"test": "test"}).get_content())
