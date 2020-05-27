"""Terminal Driver Module."""

import logging

from ...app import App
from ...contracts.MailContract import MailContract
from ...drivers import BaseMailDriver


class MailTerminalDriver(BaseMailDriver, MailContract):
    """Mail terminal driver."""

    def __init__(self, app: App):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
        self.logger.handlers = []
        handler = logging.StreamHandler()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def send(self, message=None):
        """Prints the message to the terminal.

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
