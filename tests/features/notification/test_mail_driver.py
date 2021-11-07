from tests import TestCase
from src.masonite.notification import Notification, Notifiable
from src.masonite.mail import Mailable
from masoniteorm.models import Model


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


class TestMailDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    def test_send_to_anonymous(self):
        self.notification.route("mail", "test@mail.com").send(WelcomeNotification())

    def test_send_to_notifiable(self):
        user = User.find(1)
        user.notify(WelcomeUserNotification())

    def test_send_and_override_driver(self):
        # TODO: but I don't really know how to proceed as driver can't be defined anymore
        # in the Mailable
        # Some API solutions:
        # self.notification.route("mail", "test@mail.com").send(WelcomeNotification()).driver("log")
        # self.notification.route("mail", "test@mail.com").send(WelcomeNotification(), driver="log")
        # self.notification.route("mail", "test@mail.com", driver="log").send(WelcomeNotification())
        pass
