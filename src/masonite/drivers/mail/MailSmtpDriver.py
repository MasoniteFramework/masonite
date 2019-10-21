"""SMTP Driver Module."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from masonite.contracts.MailContract import MailContract
from masonite.drivers import BaseMailDriver


class MailSmtpDriver(BaseMailDriver, MailContract):
    """Mail smtp driver."""

    def send(self, message_contents=None):
        """Send the message through SMTP.

        Keyword Arguments:
            message {string} -- The message to be sent to SMTP. (default: {None})

        Returns:
            None
        """
        config = self.config.DRIVERS['smtp']

        message = MIMEMultipart('alternative')

        if not message_contents:
            message_contents = self.message_body

        message_contents = MIMEText(message_contents, 'html')

        message['Subject'] = self.message_subject
        message['From'] = '{0} <{1}>'.format(
            self.config.FROM['name'], self.config.FROM['address'])
        message['To'] = self.to_address
        message.attach(message_contents)

        # Send the message via our own SMTP server.
        if 'ssl' in config and config['ssl'] is True:
            self.smtp = smtplib.SMTP_SSL('{0}:{1}'.format(config['host'], config['port']))
        else:
            self.smtp = smtplib.SMTP('{0}:{1}'.format(
                config['host'], config['port']))

        self.smtp.login(config['username'], config['password'])

        if self._queue:
            from wsgi import container
            from masonite import Queue
            container.make(Queue).push(
                self._send_mail,
                args=(self.config.FROM['name'], self.to_address, message.as_string())
            )
            return

        self._send_mail(self.config.FROM['name'],
                self.to_address, message.as_string())

    def _send_mail(self, *args):
        """Wrapper around sending mail so it can also be used for queues."""
        self.smtp.sendmail(*args)
        self.smtp.quit()
