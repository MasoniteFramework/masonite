from tests.features.notification.test_anonymous_notifiable import WelcomeNotification
from tests import TestCase
from src.masonite.mail import Mailable
from src.masonite.notification import Notification, SlackMessage, Sms, Notifiable
from masoniteorm.models import Model


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password"]

    def route_notification_for_broadcast(self):
        return f"user.{self.id}"

    def route_notification_for_slack(self):
        return "#bot"

    def route_notification_for_vonage(self):
        return "+33123456789"

    def route_notification_for_mail(self):
        return self.email


class WelcomeNotification(Notification):
    def to_mail(self, notifiable):
        return (
            Mailable()
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
        )

    def to_database(self, notifiable):
        return {"data": "Welcome {0}!".format(notifiable.name)}

    def to_broadcast(self, notifiable):
        return {"data": "Welcome"}

    def to_slack(self, notifiable):
        return SlackMessage().text("Welcome !").from_("test-bot")

    def to_vonage(self, notifiable):
        return Sms().text("Welcome !").from_("123456")

    def via(self, notifiable):
        return ["mail", "database", "slack", "vonage", "broadcast"]


class TestIntegrationsNotifications(TestCase):
    def setUp(self):
        super().setUp()
        self.fake("notification")

    def tearDown(self):
        super().tearDown()
        self.restore("notification")

    def test_all_drivers_with_anonymous(self):
        notif = (
            self.application.make("notification")
            .route("mail", "user@example.com")
            .route("slack", "#general")
            .route("broadcast", "all")
            .route("vonage", "+33456789012")
        )
        notif.send(WelcomeNotification()).assertSentTo(
            "user@example.com", WelcomeNotification
        ).assertSentTo("#general", WelcomeNotification).assertSentTo(
            "all", WelcomeNotification
        ).assertSentTo(
            "+33456789012", WelcomeNotification
        )

    def test_all_drivers_with_notifiable(self):
        self.application.make("notification").assertNothingSent()
        user = User.find(1)
        user.notify(WelcomeNotification())
        self.application.make("notification").assertSentTo(
            "user@example.com", WelcomeNotification
        ).assertSentTo("#general", WelcomeNotification).assertSentTo(
            "all", WelcomeNotification
        ).assertSentTo(
            "+33456789012", WelcomeNotification
        )
