from tests import TestCase

from src.masonite.notification import Notification, Notifiable, SlackMessage
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


class OtherNotification(Notification):
    def to_mail(self, notifiable):
        return (
            Mailable()
            .subject("Other")
            .from_("sam@masoniteproject.com")
            .text("Hello again!")
        )

    def via(self, notifiable):
        return ["mail"]


class OrderNotification(Notification):
    def __init__(self, order_id):
        self.order_id = order_id

    def to_mail(self, notifiable):
        return (
            Mailable()
            .subject(f"Order {self.order_id} shipped !")
            .from_("sam@masoniteproject.com")
            .text(f"{notifiable.name}, your order has been shipped")
        )

    def to_slack(self, notifiable):
        return SlackMessage().text(f"Order {self.order_id} has been shipped !")

    def via(self, notifiable):
        return ["mail", "slack"]


class TestMockNotification(TestCase):
    def setUp(self):
        super().setUp()
        self.fake("notification")

    def tearDown(self):
        super().tearDown()
        self.restore("notification")

    def test_assert_nothing_sent(self):
        notification = self.application.make("notification")
        notification.assertNothingSent()

    def test_assert_count(self):
        notification = self.application.make("notification")
        notification.assertCount(0)
        notification.route("mail", "test@mail.com").send(WelcomeNotification())
        notification.assertCount(1)
        notification.route("mail", "test2@mail.com").send(WelcomeNotification())
        notification.assertCount(2)

    def test_reset_count(self):
        notification = self.application.make("notification")
        notification.assertNothingSent()
        notification.route("mail", "test@mail.com").send(WelcomeNotification())
        notification.resetCount()
        notification.assertNothingSent()

    def test_assert_sent_to_with_anonymous(self):
        notification = self.application.make("notification")
        notification.route("mail", "test@mail.com").send(WelcomeNotification())
        notification.assertSentTo("test@mail.com", WelcomeNotification)

        notification.route("vonage", "123456").route("slack", "#general").send(
            WelcomeNotification()
        )
        notification.assertSentTo("123456", WelcomeNotification)
        notification.assertSentTo("#general", WelcomeNotification)

    def test_assert_not_sent_to(self):
        notification = self.application.make("notification")
        notification.resetCount()
        notification.assertNotSentTo("test@mail.com", WelcomeNotification)
        notification.route("vonage", "123456").send(OtherNotification())
        notification.assertNotSentTo("123456", WelcomeNotification)
        notification.assertNotSentTo("test@mail.com", OtherNotification)

    def test_assert_sent_to_with_notifiable(self):
        notification = self.application.make("notification")
        user = User.find(1)
        user.notify(WelcomeNotification())
        notification.assertSentTo(user, WelcomeNotification)
        user.notify(OtherNotification())
        notification.assertSentTo(user, OtherNotification)
        notification.assertCount(2)

    def test_assert_sent_to_with_count(self):
        notification = self.application.make("notification")
        user = User.find(1)
        user.notify(WelcomeNotification())
        user.notify(WelcomeNotification())
        notification.assertSentTo(user, WelcomeNotification, count=2)

        user.notify(OtherNotification())
        user.notify(OtherNotification())
        with self.assertRaises(AssertionError):
            notification.assertSentTo(user, OtherNotification, count=1)

    def test_assert_with_assertions_on_notification(self):
        user = User.find(1)
        user.notify(OrderNotification(6))
        self.application.make("notification").assertSentTo(
            user,
            OrderNotification,
            lambda user, notification: (
                notification.assertSentVia("mail", "slack")
                .assertEqual(notification.order_id, 6)
                .assertEqual(
                    notification.to_mail(user).get_options().get("subject"),
                    "Order 6 shipped !",
                )
                .assertIn(
                    user.name,
                    notification.to_mail(user).get_options().get("text_content"),
                )
            ),
        )

    def test_last_notification(self):
        notification = self.application.make("notification")
        message = WelcomeNotification()
        notification.route("mail", "test@mail.com").send(message)
        assert message == notification.last()

    def test_assert_last(self):
        self.application.make("notification").route("mail", "test@mail.com").route(
            "slack", "#general"
        ).send(OrderNotification(10))
        self.application.make("notification").assertLast(
            lambda user, notif: (
                notif.assertSentVia("mail")
                .assertEqual(notif.order_id, 10)
                .assertEqual(
                    notif.to_slack(user).get_options().get("text"),
                    "Order 10 has been shipped !",
                )
            )
        )
