"""Log Driver Module."""

import logging
import os

from ...app import App
from ...contracts import MailContract
from ...drivers import BaseMailDriver


class MailLogDriver(BaseMailDriver, MailContract):
    """Mail log driver."""
    def __init__(self, app: App):
        super().__init__(app)

        if 'log' in self.config.DRIVERS and 'location' in self.config.DRIVERS['log']:
            log_location = self.config.DRIVERS['log']['location']
        else:
            log_location = 'bootstrap/mail'

        if not os.path.exists(log_location):
            # Create the path to the model if it does not exist
            os.makedirs(log_location)

        handler = logging.FileHandler('{0}/{1}'.format(
            log_location,
            os.getenv('MAIL_LOGFILE', 'mail.log')
        ), delay=True)
        self.logger = logging.getLogger(__name__)
        self.logger.handlers = []
        self.logger.propagate = False
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def send(self, message=None):
        """Prints the message in a log.

        Keyword Arguments:
            message {string} -- The message to be printed. (default: { None })

        Returns:
            None
        """

        if not message:
            message = self.message_body

        self.logger.info('***************************************')

        self.logger.info('To: {}'.format(self.mail_to_header))
        self.logger.info('From: {}'.format(self.mail_from_header))
        self.logger.info('Subject: {}'.format(self.message_subject))
        self.logger.info('Reply-To: {}'.format(self.message_reply_to))
        self.logger.info('Message: ')
        self.logger.info(message)

        self.logger.info('***************************************')
