import pytest
from unittest.mock import patch, MagicMock
from tests import TestCase
from src.masonite.notification import Notification, Notifiable
from masoniteorm.models import Model


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password"]

    def route_notification_for_broadcast(self):
        return f"user.{self.id}"


class WelcomeNotification(Notification):
    def to_broadcast(self, notifiable):
        return {"data": "Welcome"}

    def via(self, notifiable):
        return ["broadcast"]


@pytest.mark.integrations
class TestBroadcastDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    def test_send_to_anonymous(self):
        # Patch get_connection so the PusherDriver never touches pusher.Pusher
        # and there's no cached connection across tests.
        mock_conn = MagicMock()
        mock_conn.trigger.return_value = {"status": 200}
        with patch(
            "src.masonite.broadcasting.drivers.PusherDriver.PusherDriver.get_connection",
            return_value=mock_conn,
        ):
            self.notification.route("broadcast", "all").send(WelcomeNotification())
        mock_conn.trigger.assert_called_once()

    def test_send_to_notifiable(self):
        mock_conn = MagicMock()
        mock_conn.trigger.return_value = {"status": 200}
        with patch(
            "src.masonite.broadcasting.drivers.PusherDriver.PusherDriver.get_connection",
            return_value=mock_conn,
        ):
            user = User.find(1)
            user.notify(WelcomeNotification())
        mock_conn.trigger.assert_called_once()
