"""Mailgun Driver Module."""
import warnings

import requests

from ...contracts.MailContract import MailContract
from ...drivers import BaseMailDriver


class MailMailgunDriver(BaseMailDriver, MailContract):
    """Mailgun driver."""

    def message(self):
        data = {
            'from': self.mail_from_header,
            'to': self.to_addresses,
            'subject': self.message_subject,
            'h:Reply-To': self.message_reply_to,
        }

        # Attach both mimetypes if they exist.
        if self.text_content:
            data['text'] = self.text_content
        if self.html_content:
            data['html'] = self.html_content

        return data

    def send(self, message=None):
        """Send the message through the Mailgun service.

        Keyword Arguments:
            message {string} -- The message to be sent to Mailgun. (default: {None})

        Returns:
            requests.post -- Returns the response as a requests object.
        """
        if message and isinstance(message, str):
            warnings.warn(
                'Passing message to .send() is deprecated. Please use .text() and .html().',
                category=DeprecationWarning,
                stacklevel=2)
            data = self._get_message_for_send_deprecated(message)

        # The above should be removed once deprecation time period passed.
        elif not message:
            data = self.message()
        else:
            data = message

        if self._queue:
            from wsgi import container
            from ... import Queue
            return container.make(Queue).push(self._send_mail, args=(data,))

        return self._send_mail(data)

    def _send_mail(self, data):
        """Wrapper around sending mail so it can also be used with queues.

        Arguments:
            data {dict} -- The data for mailgun post request.

        Returns:
            requests.post
        """

        domain = self.config.DRIVERS['mailgun']['domain']
        secret = self.config.DRIVERS['mailgun']['secret']

        return requests.post(
            "https://api.mailgun.net/v3/{0}/messages".format(domain),
            auth=("api", secret),
            data=data)
