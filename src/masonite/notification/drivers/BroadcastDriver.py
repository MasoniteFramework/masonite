"""Broadcast notification driver."""

from .BaseDriver import BaseDriver


class BroadcastDriver(BaseDriver):
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def send(self, notifiable, notification):
        """Used to broadcast a notification."""
        data = self.get_data("broadcast", notifiable, notification)
        channels = notification.broadcast_on() or notifiable.route_notification_for(
            "broadcast"
        )
        event = notification.type()
        self.application.make("broadcast").channel(channels, event, data)
