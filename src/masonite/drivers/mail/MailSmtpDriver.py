"""SMTP Driver Module."""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ...contracts.MailContract import MailContract
from ...drivers import BaseMailDriver


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
        message['From'] = self.mail_from_header
        message['To'] = self.mail_to_header
        message['Reply-To'] = self.message_reply_to
        message.attach(message_contents)

        # Send the message via our own SMTP server.
        if 'ssl' in config and config['ssl'] is True:
            self.smtp = smtplib.SMTP_SSL('{0}:{1}'.format(config['host'], config['port']))
        else:
            self.smtp = smtplib.SMTP('{0}:{1}'.format(
                config['host'], config['port']))

        # Check if TLS enabled
        if 'tls' in config and config['tls'] is True:
            # Define secure TLS connection
            context = ssl.create_default_context()
            context.check_hostname = False

            # Check if correct response code for starttls is received from the server
            if self.smtp.starttls(context=context)[0] != 220:
                raise smtplib.SMTPNotSupportedError("Server is using untrusted protocol.")

        if config.get('login', True):
            self.smtp.login(config['username'], config['password'])

        if self._queue:
            from wsgi import container
            from ... import Queue
            container.make(Queue).push(
                self._send_mail,
                args=(self.mail_from_header, self.to_addresses, message.as_string())
            )
            return

        self._send_mail(self.mail_from_header, self.to_addresses, message.as_string())

    def _send_mail(self, *args):
        """Wrapper around sending mail so it can also be used for queues."""
        self.smtp.sendmail(*args)
        self.smtp.quit()
