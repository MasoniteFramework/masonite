"""Anonymous Notifiable mixin"""

from .Notifiable import Notifiable


class AnonymousNotifiable(Notifiable):
    """Anonymous notifiable allowing to send notification without having
    a notifiable entity.

    Usage:
        self.notification.route("sms", "+3346474764").send(WelcomeNotification())
    """

    def __init__(self, application=None):
        self.application = application
        self._routes = {}

    def route(self, driver, recipient):
        """Define which driver using to route the notification."""
        if driver == "database":
            raise ValueError(
                "The database driver does not support on-demand notifications."
            )
        self._routes[driver] = recipient
        return self

    def route_notification_for(self, driver):
        try:
            return self._routes[driver]
        except KeyError:
            raise ValueError(
                "Routing has not been defined for the driver {}".format(driver)
            )

    def send(self, notification, dry=False, fail_silently=False):
        """Send the given notification."""
        return self.application.make("notification").send(
            self, notification, self._routes, dry, fail_silently
        )
