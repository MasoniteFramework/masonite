from tests import TestCase

from src.masonite.notification import Notification, AnonymousNotifiable
from src.masonite.mail import Mailable


class WelcomeNotification(Notification):
    def to_mail(self, notifiable):
        return Mailable().text("Welcome")

    def via(self, notifiable):
        return ["mail"]


class TestAnonymousNotifiable(TestCase):
    def test_one_routing(self):
        notifiable = AnonymousNotifiable(self.application).route(
            "mail", "user@example.com"
        )
        self.assertDictEqual({"mail": "user@example.com"}, notifiable._routes)

    def test_multiple_routing(self):
        notifiable = (
            AnonymousNotifiable(self.application)
            .route("mail", "user@example.com")
            .route("slack", "#general")
        )
        self.assertDictEqual(
            {"mail": "user@example.com", "slack": "#general"}, notifiable._routes
        )

    def test_sending_notification(self):
        self.application.make("notification").route("mail", "user@example.com").send(
            WelcomeNotification()
        )

    def test_can_override_dry_when_sending(self):
        AnonymousNotifiable(self.application).route("mail", "user@example.com").send(
            WelcomeNotification(), dry=True
        )
        self.application.make("notification").dry_notifications.keys() == 1

    def test_can_override_fail_silently_when_sending(self):
        class FailingNotification(Notification):
            def to_slack(self, notifiable):
                raise Exception("Error")

            def via(self, notifiable):
                return ["slack"]

        AnonymousNotifiable(self.application).route("slack", "#general").send(
            FailingNotification(), fail_silently=True
        )
        # no assertion raised :)
