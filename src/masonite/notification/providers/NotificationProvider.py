from ...providers import Provider
from ...utils.structures import load
from ..drivers import (
    BroadcastDriver,
    DatabaseDriver,
    MailDriver,
    SlackDriver,
    VonageDriver,
)
from ...configuration import config

from ..NotificationManager import NotificationManager
from ..MockNotification import MockNotification
from ..commands import MakeNotificationCommand, NotificationTableCommand


class NotificationProvider(Provider):
    """Notifications Provider"""

    def __init__(self, application):
        self.application = application

    def register(self):
        notification_manager = NotificationManager(self.application).set_configuration(
            config("notification")
        )
        notification_manager.add_driver("mail", MailDriver(self.application))
        notification_manager.add_driver("vonage", VonageDriver(self.application))
        notification_manager.add_driver("slack", SlackDriver(self.application))
        notification_manager.add_driver("database", DatabaseDriver(self.application))
        notification_manager.add_driver("broadcast", BroadcastDriver(self.application))

        self.application.bind("notification", notification_manager)
        self.application.bind("mock.notification", MockNotification)
        self.application.make("commands").add(
            MakeNotificationCommand(self.application),
            NotificationTableCommand(),
        )

    def boot(self):
        pass
