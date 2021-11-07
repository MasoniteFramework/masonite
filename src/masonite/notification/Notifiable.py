"""Notifiable mixin"""
from masoniteorm.relationships import has_many

from .DatabaseNotification import DatabaseNotification
from ..exceptions.exceptions import NotificationException


class Notifiable:
    """Notifiable mixin allowing to send notification to a model. It's often used with the
    User model.

    Usage:
        user.notify(WelcomeNotification())
    """

    def notify(self, notification, drivers=[], dry=False, fail_silently=False):
        """Send the given notification."""
        from wsgi import application

        return application.make("notification").send(
            self, notification, drivers, dry, fail_silently
        )

    def route_notification_for(self, driver):
        """Get the notification routing information for the given driver. If method has not been
        defined on the model: for mail driver try to use 'email' field of model."""
        # check if routing has been specified on the model
        method_name = "route_notification_for_{0}".format(driver)

        try:
            method = getattr(self, method_name)
            return method()
        except AttributeError:
            # if no method is defined on notifiable use default
            if driver == "database":
                # with database channel, notifications are saved to database
                pass
            elif driver == "mail":
                return self.email
            else:
                raise NotificationException(
                    "Notifiable model does not implement {}".format(method_name)
                )

    @has_many("id", "notifiable_id")
    def notifications(self):
        """Get all notifications sent to the model instance. Only for 'database'
        notifications."""
        return DatabaseNotification.where("notifiable_type", "users").order_by(
            "created_at", direction="DESC"
        )

    @property
    def unread_notifications(self):
        """Get the model instance unread notifications. Only for 'database'
        notifications."""
        return self.notifications.where("read_at", "==", None)

    @property
    def read_notifications(self):
        """Get the model instance read notifications. Only for 'database'
        notifications."""
        return self.notifications.where("read_at", "!=", None)
