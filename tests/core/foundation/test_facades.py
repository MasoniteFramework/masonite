from tests import TestCase
from src.masonite.facades import Mail, View


class TestFacades(TestCase):
    def test_mail_facade(self):
        self.assertEqual(
            Mail.get_config_options("mailgun")["from"], "no-reply@masonite.com"
        )

    def test_view_facade(self):
        View.add_location("tests/integrations/templates")
        self.assertEqual("test", View.render("test", {"test": "test"}).get_content())
