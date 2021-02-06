from masonite.drivers.mail.Mailable import Mailable
from tests.core.test_mail_log_drivers import UserMock
from src.masonite.testing import TestCase
from src.masonite.drivers.mail.BaseMailDriver import BaseMailDriver as Mail


class TestMailable(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .send_from("admin@test.com")
            .view("emails.test", {"user": "Sam"})
            .reply_to("customer@email.com")
            .subject("Forgot Password")
        )


class TestMockMail(TestCase):
    def setUp(self):
        super().setUp()
        self.mail = Mail.fake()

    def tearDown(self):
        super().tearDown()
        self.mail = Mail.restore()

    def test_mocking_mailgun(self):
        self.mail.driver("mailgun").to("user@example.com").html(
            "<div>Hello</div>"
        ).send()
        self.mail.assertCountAll(1)

    def test_mocking_log(self):
        user = UserMock
        user.email = "test@email.com"
        self.mail.assertNothingSent()
        self.mail.driver("log").to(user).reply_to("reply-to@email.com").send("Masonite")
        self.mail.driver("log").to(user).reply_to("reply-to@email.com").send("Masonite")
        self.mail.assertCountAll(2)

    def test_mailable(self):
        self.mail.driver("smtp").mailable(TestMailable()).send()
        self.mail.driver("smtp").mailable(TestMailable()).send()
        self.mail.assertSent(TestMailable, count=2)

    def test_mailable_with_custom_assertions(self):
        self.mail.driver("smtp").mailable(TestMailable()).send()
        self.mail.assertSent(
            TestMailable,
            lambda mailable: mailable.hasSubject("Forgot Password")
            .hasTo("idmann509@gmail.com")
            .hasReplyTo("customer@email.com")
            .isSentFrom("admin@test.com")
            .hasView("emails.test")
            .hasInContext("user")
            .hasInContext("user", "Sam")
            .hasContext({"user": "Sam"}),
        )

    def test_assert_sent_to(self):
        user = UserMock
        user.email = "test@email.com"
        self.mail.driver("log").to(user).reply_to("reply-to@email.com").send("Masonite")
        self.mail.assertLast().hasTo(user.email)

        self.mail.driver("smtp").mailable(TestMailable()).send()
        self.mail.assertSentTo("idmann509@gmail.com", TestMailable)

    def test_assert_email_content_unified(self):
        self.mail.driver("mailgun").to("user@example.com").html(
            "<div>Hello</div>"
        ).send()
        self.mail.assertLast().hasTo("user@example.com").seeIn("<div>Hello</div>")

        self.mail.driver("smtp").mailable(TestMailable()).send()
        self.mail.assertLast().hasTo("idmann509@gmail.com").hasView(
            "emails.test"
        ).seeIn("testing email")
