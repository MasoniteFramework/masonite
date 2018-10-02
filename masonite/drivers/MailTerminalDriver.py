""" Terminal Driver Module """

import logging

from masonite.contracts.MailContract import MailContract
from masonite.drivers.BaseMailDriver import BaseMailDriver


class MailTerminalDriver(BaseMailDriver, MailContract):
    """Mail terminal driver
    """

    def __init__(self, MailConfig, View):
        super().__init__(MailConfig, View)

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

        self.logger.info('To: {}'.format(self.to_address))
        self.logger.info('From: {0} <{1}>'.format(
            self.config.FROM['name'], self.config.FROM['address']))
        self.logger.info('Subject: {}'.format(self.message_subject))
        self.logger.info('Message: ')
        self.logger.info(message)

        self.logger.info('***************************************')
