from tests import TestCase
from unittest.mock import patch, MagicMock
from src.masonite.notification import Notification, Notifiable, Sms, Textable
from src.masonite.exceptions import NotificationException

from masoniteorm.models import Model
from vonage_sms.responses import SmsResponse, MessageResponse
from vonage_sms.errors import SmsError


def _ok_response():
    """Build a successful SmsResponse for use in mocks."""
    return SmsResponse(**{
        "message-count": "1",
        "messages": [{
            "to": "+33123456789",
            "message-id": "140000012BD37332",
            "status": "0",
            "remaining-balance": "1.87440000",
            "message-price": "0.06280000",
            "network": "20810",
        }],
    })


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


class TestVonageDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    def test_sending_without_credentials(self):
        """vonage 4.x raises SmsError on bad credentials; driver wraps it."""
        with patch(
            "vonage_sms.sms.Sms.send",
            side_effect=SmsError(
                "Sms.send_message method failed with error code 2: Missing api_key"
            ),
        ):
            with self.assertRaises(NotificationException) as ctx:
                self.notification.route("vonage", "+33123456789").send(
                    WelcomeNotification()
                )
        self.assertIn("Code [2]", str(ctx.exception))

    def test_send_to_anonymous(self):
        with patch("vonage_sms.sms.Sms.send", return_value=_ok_response()):
            self.notification.route("vonage", "+33123456789").send(
                WelcomeNotification()
            )

    def test_send_to_notifiable(self):
        with patch("vonage_sms.sms.Sms.send", return_value=_ok_response()):
            user = User.find(1)
            user.notify(WelcomeUserNotification())

    def test_send_to_notifiable_with_route_notification_for(self):
        with patch("vonage_sms.sms.Sms.send", return_value=_ok_response()):
            user = User.find(1)
            user.notify(WelcomeNotification())

    def test_global_send_from_is_used_when_not_specified(self):
        notifiable = self.notification.route("vonage", "+33123456789")
        sms = self.notification.get_driver("vonage").build(
            notifiable, OtherNotification()
        )
        self.assertEqual(sms._from, "+33000000000")
