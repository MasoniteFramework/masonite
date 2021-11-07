from tests import TestCase
from unittest.mock import patch
from src.masonite.notification import Notification, Notifiable, Sms, Textable
from src.masonite.exceptions import NotificationException

from masoniteorm.models import Model


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password", "phone"]

    def route_notification_for_vonage(self):
        return "+33123456789"


class WelcomeUserNotification(Notification, Textable):
    def to_vonage(self, notifiable):
        return self.text_message("Welcome !").from_("123456")

    def via(self, notifiable):
        return ["vonage"]


class WelcomeNotification(Notification):
    def to_vonage(self, notifiable):
        return Sms().text("Welcome !").from_("123456")

    def via(self, notifiable):
        return ["vonage"]

    def should_send(self):
        return True


class OtherNotification(Notification):
    def to_vonage(self, notifiable):
        return Sms().text("Welcome !")

    def via(self, notifiable):
        return ["vonage"]


class VonageAPIMock(object):
    @staticmethod
    def send_success():
        return {"hoho": "hihi", "message-count": 1, "messages": [{"status": "0"}]}

    @staticmethod
    def send_error(error="Missing api_key", status=2):
        return {
            "message-count": 1,
            "messages": [{"status": str(status), "error-text": error}],
        }


class TestVonageDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    def test_sending_without_credentials(self):
        with self.assertRaises(NotificationException) as e:
            self.notification.route("vonage", "+33123456789").send(
                WelcomeNotification()
            )
        error_message = str(e.exception)
        self.assertIn("Code [2]", error_message)

    def test_send_to_anonymous(self):
        with patch("vonage.sms.Sms") as MockSmsClass:
            MockSmsClass.return_value.send_message.return_value = (
                VonageAPIMock().send_success()
            )
            self.notification.route("vonage", "+33123456789").send(
                WelcomeNotification()
            )

    def test_send_to_notifiable(self):
        with patch("vonage.sms.Sms") as MockSmsClass:
            MockSmsClass.return_value.send_message.return_value = (
                VonageAPIMock().send_success()
            )
            user = User.find(1)
            user.notify(WelcomeUserNotification())

    def test_send_to_notifiable_with_route_notification_for(self):
        with patch("vonage.sms.Sms") as MockSmsClass:
            MockSmsClass.return_value.send_message.return_value = (
                VonageAPIMock().send_success()
            )
            user = User.find(1)
            user.notify(WelcomeNotification())

    def test_global_send_from_is_used_when_not_specified(self):
        notifiable = self.notification.route("vonage", "+33123456789")
        sms = self.notification.get_driver("vonage").build(
            notifiable, OtherNotification()
        )
        self.assertEqual(sms._from, "+33000000000")
