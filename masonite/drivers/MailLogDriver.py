""" Log Driver Module """

import logging

from masonite.contracts.MailContract import MailContract
from masonite.drivers.BaseMailDriver import BaseMailDriver

logging.basicConfig(level=logging.DEBUG)


class MailLogDriver(BaseMailDriver, MailContract):
    """Mail log driver
    """

    def send(self, message=None):
        """Sends the message through SMTP.

        Keyword Arguments:
            message {string} -- The message to be printed. (default: { None })

        Returns:
            None
        """

        if not message:
            message = self.message_body

        logging.debug('***************************************')

        logging.debug('To: {}'.format(self.to_address))
        logging.debug('From: {0} <{1}>'.format(
            self.config.FROM['name'], self.config.FROM['address']))
        logging.debug('Subject: {}'.format(self.message_subject))
        logging.debug('Message: ')
        logging.debug(message)

        logging.debug('***************************************')


