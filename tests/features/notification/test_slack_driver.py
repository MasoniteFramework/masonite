import pytest
import responses
from tests import TestCase
from src.masonite.notification import Notification, Notifiable, SlackMessage
from src.masonite.exceptions import NotificationException

from masoniteorm.models import Model

# fake webhook for tests
webhook_url = "https://hooks.slack.com/services/X/Y/Z"
webhook_url_2 = "https://hooks.slack.com/services/A/B/C"


def route_for_slack(self):
    return "#bot"


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password", "phone"]

    def route_notification_for_slack(self):
        return route_for_slack(self)


class WelcomeUserNotification(Notification):
    def to_slack(self, notifiable):
        return SlackMessage().text(f"Welcome {notifiable.name}!").from_("test-bot")

    def via(self, notifiable):
        return ["slack"]


class WelcomeNotification(Notification):
    def to_slack(self, notifiable):
        return SlackMessage().text("Welcome !").from_("test-bot")

    def via(self, notifiable):
        return ["slack"]


class OtherNotification(Notification):
    def to_slack(self, notifiable):
        return (
            SlackMessage().to(["#general", "#news"]).text("Welcome !").from_("test-bot")
        )

    def via(self, notifiable):
        return ["slack"]


class TestSlackWebhookDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    @responses.activate
    def test_sending_to_anonymous(self):
        responses.add(responses.POST, webhook_url, body=b"ok")
        self.notification.route("slack", webhook_url).notify(WelcomeNotification())
        self.assertTrue(responses.assert_call_count(webhook_url, 1))

    @responses.activate
    def test_sending_to_notifiable(self):
        responses.add(responses.POST, webhook_url, body=b"ok")
        User.route_notification_for_slack = lambda notifiable: webhook_url
        user = User.find(1)
        user.notify(WelcomeNotification())
        self.assertTrue(responses.assert_call_count(webhook_url, 1))
        User.route_notification_for_slack = route_for_slack

    @responses.activate
    def test_sending_to_multiple_webhooks(self):
        responses.add(responses.POST, webhook_url, body=b"ok")
        responses.add(responses.POST, webhook_url_2, body=b"ok")
        User.route_notification_for_slack = lambda notifiable: [
            webhook_url,
            webhook_url_2,
        ]
        user = User.find(1)
        user.notify(WelcomeNotification())
        self.assertTrue(responses.assert_call_count(webhook_url, 1))
        self.assertTrue(responses.assert_call_count(webhook_url_2, 1))
        User.route_notification_for_slack = route_for_slack


class TestSlackAPIDriver(TestCase):
    url = "https://slack.com/api/chat.postMessage"
    channel_url = "https://slack.com/api/conversations.list"

    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    def test_sending_without_credentials(self):
        with self.assertRaises(NotificationException) as e:
            self.notification.route("slack", "123456").notify(WelcomeNotification())
        self.assertIn("not_authed", str(e.exception))

    @responses.activate
    def test_sending_to_anonymous(self):
        responses.add(
            responses.POST,
            self.url,
            body=b'{"ok": "True"}',
        )
        responses.add(
            responses.POST,
            self.channel_url,
            body=b'{"channels": [{"name": "bot", "id": "123"}]}',
        )
        self.notification.route("slack", "#bot").notify(WelcomeNotification())
        # to convert #bot to Channel ID
        self.assertTrue(responses.assert_call_count(self.channel_url, 1))
        self.assertTrue(responses.assert_call_count(self.url, 1))

    @responses.activate
    def test_sending_to_notifiable(self):
        user = User.find(1)
        responses.add(
            responses.POST,
            self.url,
            body=b'{"ok": "True"}',
        )
        responses.add(
            responses.POST,
            self.channel_url,
            body=b'{"channels": [{"name": "bot", "id": "123"}]}',
        )
        user.notify(WelcomeUserNotification())
        self.assertTrue(responses.assert_call_count(self.url, 1))

    @responses.activate
    @pytest.mark.skip(
        reason="Failing because user defined routing takes precedence. What should be the behaviour ?"
    )
    def test_sending_to_multiple_channels(self):
        user = User.find(1)
        responses.add(
            responses.POST,
            self.url,
            body=b'{"ok": "True"}',
        )
        responses.add(
            responses.POST,
            self.channel_url,
            body=b'{"channels": [{"name": "bot", "id": "123"}, {"name": "general", "id": "456"}]}',
        )
        user.notify(OtherNotification())
        self.assertTrue(responses.assert_call_count(self.channel_url, 2))
        self.assertTrue(responses.assert_call_count(self.url, 2))

    @responses.activate
    def test_convert_channel(self):
        channel_id = self.notification.get_driver("slack").convert_channel(
            "123456", "token"
        )
        self.assertEqual(channel_id, "123456")

        responses.add(
            responses.POST,
            self.channel_url,
            body=b'{"channels": [{"name": "general", "id": "654321"}]}',
        )
        channel_id = self.notification.get_driver("slack").convert_channel(
            "#general", "token"
        )
        self.assertEqual(channel_id, "654321")
