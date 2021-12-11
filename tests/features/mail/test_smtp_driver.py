from tests import TestCase
from src.masonite.mail import Mailable
import pytest


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .header("X-Custom", "value")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )


@pytest.mark.integrations
class TestSMTPDriver(TestCase):
    def test_send_mailable(self):
        self.application.make("mail").mailable(Welcome()).send(driver="terminal")
