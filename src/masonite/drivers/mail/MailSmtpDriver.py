"""SMTP Driver Module."""

import smtplib
import ssl
import warnings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ...contracts.MailContract import MailContract
from ...drivers import BaseMailDriver


class MailSmtpDriver(BaseMailDriver, MailContract):
    """Mail smtp driver."""

    def message(self):
        """Creates a message object for the underlying driver.

        Returns:
            email.mime.multipart.MIMEMultipart
        """
        message = MIMEMultipart('alternative')
        message['Subject'] = self.message_subject
        message['From'] = self.mail_from_header
        message['To'] = self.mail_to_header
        message['Reply-To'] = self.message_reply_to

        # Attach both mimetypes if they exist.
        if self.html_content:
            message.attach(MIMEText(self.html_content, 'html'))

        if self.text_content:
            message.attach(MIMEText(self.text_content, 'plain'))

        return message

    def send(self, message=None, message_contents=None):
        """Send the message through SMTP.

        Keyword Arguments:
            message {string} -- The HTML message to be sent to SMTP. (default: {None})

        Returns:
            None
        """
        # The old argument name was `message_contents`. users might have used this as keyword argument or as arg.
        assert message is None or message_contents is None, \
            'using deprecated  argument "message_contents" together with the new arg "message" ??'
        message_contents = message or message_contents
        if message_contents and isinstance(message_contents, str):
            warnings.warn(
                'Passing message_contents to .send() is a deprecated. Please use .text() and .html().',
                category=DeprecationWarning,
                stacklevel=2)
            message = self._get_message_for_send_deprecated(message_contents)

        # The above should be removed once deprecation time period passed.
        elif not message:
            message = self.message()

        self._smtp_connect()

        if self._queue:
            from wsgi import container
            from ... import Queue
            container.make(Queue).push(
                self._send_mail,
                args=(self.mail_from_header, self.to_addresses, message)
            )
            return

        return self._send_mail(self.mail_from_header, self.to_addresses, message)

    def _smtp_connect(self):
        """Sets self.smtp to an instance of `smtplib.SMTP`
        and connects using configuration in config.DRIVERS.smtp
        Returns:
            None
        """
        config = self.config.DRIVERS['smtp']
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

    def _send_mail(self, *args):
        """Wrapper around sending mail so it can also be used for queues."""
        mail_from_header, to_addresses, message = args
        response = self.smtp.send_message(message)
        self.smtp.quit()
        return response
