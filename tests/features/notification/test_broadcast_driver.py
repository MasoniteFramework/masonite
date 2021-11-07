import pytest
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
        self.notification.route("broadcast", "all").send(WelcomeNotification())

    def test_send_to_notifiable(self):
        user = User.find(1)
        user.notify(WelcomeNotification())
