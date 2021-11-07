"""Slack notification driver"""
import requests

from ...exceptions import NotificationException
from .BaseDriver import BaseDriver


class SlackDriver(BaseDriver):

    WEBHOOK_MODE = 1
    API_MODE = 2
    send_url = "https://slack.com/api/chat.postMessage"
    channel_url = "https://slack.com/api/conversations.list"

    def __init__(self, application):
        self.application = application
        self.options = {}
        self.mode = self.WEBHOOK_MODE

    def set_options(self, options):
        self.options = options
        return self

    def send(self, notifiable, notification):
        """Used to send the notification to slack."""
        slack_message = self.build(notifiable, notification)
        if slack_message._mode == self.WEBHOOK_MODE:
            self.send_via_webhook(slack_message)
        else:
            self.send_via_api(slack_message)

    def build(self, notifiable, notification):
        """Build Slack message payload sent to Slack API or through Slack webhook."""
        slack_message = self.get_data("slack", notifiable, notification)
        recipients = self.get_recipients(notifiable)
        mode = self.get_sending_mode(recipients)
        slack_message = slack_message.mode(mode)

        if mode == self.WEBHOOK_MODE:
            slack_message = slack_message.to(recipients)
        elif mode == self.API_MODE:
            slack_message = slack_message.to(recipients)
            if not slack_message._token:
                slack_message = slack_message.token(self.options.get("token"))
        return slack_message

    def get_recipients(self, notifiable):
        recipients = notifiable.route_notification_for("slack")
        if not isinstance(recipients, (list, tuple)):
            recipients = [recipients]
        return recipients

    def get_sending_mode(self, recipients):
        modes = []
        for recipient in recipients:
            if recipient.startswith("https://hooks.slack.com"):
                modes.append(self.WEBHOOK_MODE)
            else:
                modes.append(self.API_MODE)
        if len(set(modes)) > 1:
            raise NotificationException("Slack sending mode cannot be mixed.")
        return modes[0]

    def send_via_webhook(self, slack_message):
        webhook_urls = slack_message._to
        payload = slack_message.build().get_options()
        for webhook_url in webhook_urls:
            response = requests.post(
                webhook_url,
                payload,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code != 200:
                raise NotificationException(
                    "{}. Check Slack webhooks docs.".format(response.text)
                )

    def send_via_api(self, slack_message):
        """Send Slack notification with Slack Web API as documented
        here https://api.slack.com/methods/chat.postMessage"""
        channels = slack_message._to
        for channel in channels:
            channel = self.convert_channel(channel, slack_message._token)
            # set only one recipient at a time
            slack_message.to(channel)
            payload = slack_message.build().get_options()
            response = requests.post(self.send_url, payload).json()
            if not response["ok"]:
                raise NotificationException(
                    "{}. Check Slack API docs.".format(response["error"])
                )
            else:
                return response

    def convert_channel(self, name, token):
        """Calls the Slack API to find the channel ID if not already a channel ID.

        Arguments:
            name {string} -- The channel name to find.
        """
        if "#" not in name:
            return name
        response = requests.post(self.channel_url, {"token": token}).json()
        for channel in response["channels"]:
            if channel["name"] == name.split("#")[1]:
                return channel["id"]

        raise NotificationException(
            f"The user or channel being addressed either do not exist or is invalid: {name}"
        )
