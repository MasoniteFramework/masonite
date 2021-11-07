from tests import TestCase
from src.masonite.mail import Mailable
from src.masonite.mail.Recipient import Recipient


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
            .driver("smtp")
        )


class ViewMailable(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .view("mailables.welcome", {})
        )


class TestMailable(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("mail")

    def test_build_mail(self):
        mailable = Welcome().build().get_options()
        self.assertEqual(mailable.get("to"), "idmann509@gmail.com")
        self.assertEqual(mailable.get("from"), "joe@masoniteproject.com")
        self.assertEqual(mailable.get("subject"), "Masonite 4")
        self.assertEqual(mailable.get("text_content"), "Hello from Masonite!")
        self.assertEqual(mailable.get("html_content"), "<h1>Hello from Masonite!</h1>")
        self.assertEqual(mailable.get("reply_to"), "")
        self.assertEqual(mailable.get("driver"), "smtp")

    def test_build_mailable_view(self):
        mailable = (
            ViewMailable().set_application(self.application).build().get_options()
        )
        self.assertEqual(mailable.get("html_content"), "<h1>Welcome Email</h1>")
        mailable = ViewMailable().set_application(self.application).get_response()
        self.assertEqual(mailable, "<h1>Welcome Email</h1>")

    def test_attach(self):
        self.assertTrue(
            len(
                Welcome()
                .attach("invoice", "tests/integrations/storage/invoice.pdf")
                .build()
                .get_options()
                .get("attachments")
            )
            == 1
        )

    def test_recipient(self):
        to = Recipient("idmann509@gmail.com, joe@masoniteproject.com")
        self.assertEqual(
            to.header(), "<idmann509@gmail.com>, <joe@masoniteproject.com>"
        )
        to = Recipient("Joseph Mancuso <idmann509@gmail.com>, joe@masoniteproject.com")
        self.assertEqual(
            to.header(),
            "Joseph Mancuso <idmann509@gmail.com>, <joe@masoniteproject.com>",
        )

    def test_recipient(self):
        to = Recipient("idmann509@gmail.com, joe@masoniteproject.com")
        self.assertEqual(
            to.header(), "<idmann509@gmail.com>, <joe@masoniteproject.com>"
        )
        to = Recipient("Joseph Mancuso <idmann509@gmail.com>, joe@masoniteproject.com")
        self.assertEqual(
            to.header(),
            "Joseph Mancuso <idmann509@gmail.com>, <joe@masoniteproject.com>",
        )

        to = Recipient(
            ["Joseph Mancuso <idmann509@gmail.com>", "joe@masoniteproject.com"]
        )
        self.assertEqual(
            to.header(),
            "Joseph Mancuso <idmann509@gmail.com>, <joe@masoniteproject.com>",
        )
