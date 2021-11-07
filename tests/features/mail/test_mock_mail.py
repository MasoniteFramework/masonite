from tests import TestCase
from src.masonite.mail import Mailable


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("text from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )


class TestSMTPDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.fake("mail")

    def tearDown(self):
        super().tearDown()
        self.restore("mail")

    def test_mock_mail(self):
        self.fake("mail")
        welcome_email = self.application.make("mail").mailable(Welcome()).send()
        (
            welcome_email.seeEmailCc("")
            .seeEmailBcc("")
            .seeEmailContains("Hello from Masonite!")
            .seeEmailContains("text from Masonite!")
            .seeEmailFrom("joe@masoniteproject.com")
            .seeEmailCountEquals(1)
            .send()
            .seeEmailCountEquals(2)
        )

    def test_mock_mail_sending(self):
        self.fake("mail")
        welcome_email = self.application.make("mail").mailable(Welcome())
        (welcome_email.seeEmailWasNotSent().send().seeEmailWasSent())
