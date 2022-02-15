"""Mail notification driver."""

from .BaseDriver import BaseDriver
from ...configuration import config


class MailDriver(BaseDriver):
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def send(self, notifiable, notification):
        """Used to send the email."""
        mailable = self.get_data("mail", notifiable, notification)
        if not mailable._to:
            recipients = notifiable.route_notification_for("mail")
            mailable = mailable.to(recipients)
        return self.application.make("mail").mailable(mailable).send()
