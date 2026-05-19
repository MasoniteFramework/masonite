import pytest
import responses as responses_lib

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


@pytest.mark.integrations
class TestMailgunDriver(TestCase):
    @responses_lib.activate
    def test_send_mailable(self):
        # Mock the Mailgun API so the test is not network-dependent.
        # The mock reproduces the "unconfigured domain" response that Mailgun
        # returned when the test was originally written against a real endpoint.
        responses_lib.add(
            responses_lib.POST,
            "https://api.mailgun.net/v3//messages",
            body=b"Mailgun Magnificent API",
            status=200,
            content_type="text/plain",
        )
        response = (
            self.application.make("mail")
            .mailable(
                Welcome().attach("invoice", "tests/integrations/storage/invoice.pdf")
            )
            .send(driver="mailgun")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Mailgun Magnificent API", response.content.decode("utf-8"))
