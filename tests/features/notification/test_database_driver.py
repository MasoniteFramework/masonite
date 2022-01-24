import pendulum

from masoniteorm.models import Model

from tests import TestCase
from src.masonite.tests import DatabaseTransactions
from src.masonite.notification import Notification, Notifiable
from src.masonite.notification import DatabaseNotification


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


class WelcomeNotification(Notification):
    def to_database(self, notifiable):
        return {"data": "Welcome {0}!".format(notifiable.name)}

    def via(self, notifiable):
        return ["database"]


notif_data = {
    "id": "1234",
    "read_at": None,
    "type": "TestNotification",
    "data": "test",
    "notifiable_id": 1,
    "notifiable_type": "users",
}


class TestDatabaseDriver(TestCase, DatabaseTransactions):
    connection = None

    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    def test_send_to_notifiable(self):
        user = User.find(1)
        count = user.notifications.count()
        user.notify(WelcomeNotification())
        assert user.notifications.count() == count + 1

    def test_database_notification_is_created_correctly(self):
        user = User.find(1)
        notification = user.notify(WelcomeNotification())
        assert notification["id"]
        assert not notification["read_at"]
        assert notification["data"] == '{"data": "Welcome Joe!"}'
        assert notification["notifiable_id"] == user.id
        assert notification["notifiable_type"] == "users"

    def test_notify_multiple_users(self):
        User.create({"name": "sam", "email": "sam@test.com", "password": "secret"})
        users = User.all()  # == 2 users
        self.notification.send(users, WelcomeNotification())
        assert users[0].notifications.count() == 1
        assert users[1].notifications.count() == 1


class TestDatabaseNotification(TestCase, DatabaseTransactions):
    connection = None

    def test_database_notification_read_state(self):
        notification = DatabaseNotification.create(
            {
                **notif_data,
                "read_at": pendulum.now().to_datetime_string(),
            }
        )
        self.assertTrue(notification.is_read)
        notification.read_at = None
        self.assertFalse(notification.is_read)

    def test_database_notification_unread_state(self):
        notification = DatabaseNotification.create(
            {
                **notif_data,
                "read_at": pendulum.yesterday().to_datetime_string(),
            }
        )
        self.assertFalse(notification.is_unread)
        notification.read_at = None
        self.assertTrue(notification.is_unread)

    def test_database_notification_mark_as_read(self):
        notification = DatabaseNotification.create(notif_data)
        notification.mark_as_read()
        self.assertNotEqual(None, notification.read_at)

    def test_database_notification_mark_as_unread(self):
        notification = DatabaseNotification.create(
            {
                **notif_data,
                "read_at": pendulum.now().to_datetime_string(),
            }
        )
        notification.mark_as_unread()
        self.assertEqual(None, notification.read_at)

    def test_notifiable_get_notifications(self):
        user = User.find(1)
        self.assertEqual(0, user.notifications.count())
        user.notify(WelcomeNotification())
        self.assertEqual(1, user.notifications.count())

    def test_notifiable_get_read_notifications(self):
        user = User.find(1)
        self.assertEqual(0, user.read_notifications.count())
        DatabaseNotification.create(
            {
                **notif_data,
                "read_at": pendulum.yesterday().to_datetime_string(),
                "notifiable_id": user.id,
            }
        )
        self.assertEqual(1, user.read_notifications.count())

    def test_notifiable_get_unread_notifications(self):
        user = User.find(1)
        self.assertEqual(0, user.unread_notifications.count())
        DatabaseNotification.create(
            {
                **notif_data,
                "notifiable_id": user.id,
            }
        )
        self.assertEqual(1, user.unread_notifications.count())
