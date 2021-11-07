from tests import TestCase
from src.masonite.notification import Sms


class Welcome(Sms):
    def build(self):
        return self.to("+33612345678").from_("+44123456789").text("Masonite 4")


class TestSms(TestCase):
    def test_build_sms(self):
        sms = Welcome().build().get_options()
        self.assertEqual(sms.get("to"), "+33612345678")
        self.assertEqual(sms.get("from"), "+44123456789")
        self.assertEqual(sms.get("text"), "Masonite 4")
        self.assertEqual(sms.get("type"), "text")

    def test_set_unicode(self):
        sms = Welcome().set_unicode().build().get_options()
        self.assertEqual(sms.get("type"), "unicode")

    def test_adding_client_ref(self):
        sms = Welcome().client_ref("ABCD").build().get_options()
        self.assertEqual(sms.get("client-ref"), "ABCD")
