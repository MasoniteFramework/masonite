from masoniteorm.models import Model

from tests import TestCase
from src.masonite.notification import Notification, Notifiable
from src.masonite.mail import Mailable
from src.masonite.facades import Config


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


class WelcomeUserNotification(Notification):
    def to_mail(self, notifiable):
        return (
            Mailable()
            .to(notifiable.email)
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text(f"Hello {notifiable.name}")
        )

    def via(self, notifiable):
        return ["mail"]


class WelcomeNotification(Notification):
    def to_mail(self, notifiable):
        return (
            Mailable()
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
        )

    def via(self, notifiable):
        return ["mail"]


class CustomNotification(Notification, Mailable):
    def to_mail(self, notifiable):
        return (
            self.subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .driver("mailgun")
        )

    def via(self, notifiable):
        return ["mail"]


class TestMailDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")
        # use terminal driver as email driver for testing
        self.default_driver = Config.get("mail.drivers.default")
        Config.set("mail.drivers.default", "terminal")

    def tearDown(self):
        super().tearDown()
        Config.set("mail.drivers.default", self.default_driver)

    def test_send_to_anonymous(self):
        self.notification.route("mail", "test@mail.com").send(WelcomeNotification())

    def test_send_to_notifiable(self):
        user = User.find(1)
        user.notify(WelcomeUserNotification())

    def test_mail_driver_can_be_overriden_in_notification(self):
        mail = self.fake("mail")
        self.notification.route("mail", "test@mail.com").send(CustomNotification())
        mail.seeDriverWas("mailgun")
