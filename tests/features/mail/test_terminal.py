from tests import TestCase
from src.masonite.mail import Mailable


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )


class Other(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Other")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
            .driver("terminal")
        )


class TestTerminalDriver(TestCase):
    def test_send_mailable(self):
        self.application.make("mail").mailable(
            Welcome().attach("invoice", "tests/integrations/storage/invoice.pdf")
        ).send(driver="terminal")

    def test_define_driver_with_mailable(self):
        self.application.make("mail").mailable(
            Other().attach("invoice", "tests/integrations/storage/invoice.pdf")
        ).send()
