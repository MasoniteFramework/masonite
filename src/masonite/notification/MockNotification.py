from .NotificationManager import NotificationManager
from .AnonymousNotifiable import AnonymousNotifiable
from .Notification import Notification


class NotificationWithAsserts(Notification):
    def assertSentVia(self, *drivers):
        sent_via = self.via(self.notifiable)
        for driver in drivers:
            assert (
                driver in sent_via
            ), f"notification sent via {sent_via}, not {driver}."
        return self

    def assertEqual(self, value, reference):
        assert value == reference, "{value} not equal to {reference}."
        return self

    def assertNotEqual(self, value, reference):
        assert value != reference, "{value} equal to {reference}."
        return self

    def assertIn(self, value, container):
        assert value in container, "{value} not in {container}."
        return self

    @classmethod
    def patch(cls, target):
        for k in cls.__dict__:
            obj = getattr(cls, k)
            if not k.startswith("_") and callable(obj):
                setattr(target, k, obj)


class MockNotification(NotificationManager):
    def __init__(self, application, *args, **kwargs):
        super().__init__(application, *args, **kwargs)
        self.count = 0
        self.last_notifiable = None
        self.last_notification = None

    def send(
        self, notifiables, notification, drivers=[], dry=False, fail_silently=False
    ):
        _notifiables = []
        for notifiable in self._format_notifiables(notifiables):
            if isinstance(notifiable, AnonymousNotifiable):
                _notifiables.extend(notifiable._routes.values())
            else:
                _notifiables.append(notifiable)

        notification_key = notification.type()
        NotificationWithAsserts.patch(notification.__class__)
        for notifiable in _notifiables:
            notification.notifiable = notifiable  # for asserts
            old_notifs = self.sent_notifications.get(notifiable, {})
            old_notifs.update(
                {
                    notification_key: old_notifs.get(notification_key, [])
                    + [notification]
                }
            )
            self.sent_notifications.update({notifiable: old_notifs})
            self.count += 1
        self.last_notification = notification
        self.last_notifiable = notifiable
        return self

    def resetCount(self):
        """Reset sent notifications count."""
        self.count = 0
        self.sent_notifications = {}
        self.last_notifiable = None
        self.last_notification = None
        return self

    def assertNothingSent(self):
        assert self.count == 0, f"{self.count} notifications have been sent."
        return self

    def assertCount(self, count):
        assert (
            self.count == count
        ), f"{self.count} notifications have been sent, not {count}."
        return self

    def assertSentTo(
        self, notifiable, notification_class, callable_assert=None, count=None
    ):
        notification_key = notification_class.__name__
        notifiable_notifications = self.sent_notifications.get(notifiable, [])
        assert notification_key in notifiable_notifications
        if count:
            sent_count = len(notifiable_notifications.get(notification_key, []))
            assert (
                sent_count == count
            ), f"{notification_key} has been sent to {notifiable} {sent_count} times"
        if callable_assert:
            # assert last notification sent for this notifiable
            notification = notifiable_notifications.get(notification_key)[-1]
            assert callable_assert(notifiable, notification)
        return self

    def last(self):
        """Get last sent mocked notification if any."""
        return self.last_notification

    def assertLast(self, callable_assert):
        if not self.last_notifiable or not self.last_notification:
            raise AssertionError("No notification has been sent.")
        assert callable_assert(self.last_notifiable, self.last_notification)
        return self

    def assertNotSentTo(self, notifiable, notification_class):
        notification_key = notification_class.__name__
        notifiable_notifications = self.sent_notifications.get(notifiable, [])
        assert (
            notification_key not in notifiable_notifications
        ), f"{notification_key} has been sent to {notifiable}."
        return self
