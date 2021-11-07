from tests import TestCase

from src.masonite.notification import Notification, Notifiable
from src.masonite.mail import Mailable
from masoniteorm.models import Model


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


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


class TestNotification(TestCase):
    def test_should_send(self):
        notification = WelcomeNotification()
        self.assertTrue(notification.should_send())

    def test_ignore_errors(self):
        notification = WelcomeNotification()
        self.assertFalse(notification.ignore_errors())

    def test_notification_type(self):
        self.assertEqual("WelcomeNotification", WelcomeNotification().type())


DRY = True


class TestNotificationManager(TestCase):
    def test_dry_mode(self):
        # locally when sending to anonymous or notifiable
        self.assertEqual(
            self.application.make("notification")
            .route("mail", "test@mail.com")
            .send(WelcomeNotification(), dry=True),
            None,
        )

        user = User.find(1)
        user.notify(WelcomeNotification(), dry=True)

        # globally
        # override settings for testing purposes
        self.assertEqual(
            self.application.make("notification")
            .route("mail", "test@mail.com")
            .send(WelcomeNotification(), dry=True),
            None,
        )
