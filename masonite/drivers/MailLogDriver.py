"""Log Driver Module."""

import logging
import os

from masonite.app import App
from masonite.contracts.MailContract import MailContract
from masonite.drivers.BaseMailDriver import BaseMailDriver
from masonite.view import View


class MailLogDriver(BaseMailDriver, MailContract):
    """Mail log driver.
    """
    def __init__(self, app: App, view: View):
        super().__init__(app, view)

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
        ))
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

        self.logger.info('To: {}'.format(self.to_address))
        self.logger.info('From: {0} <{1}>'.format(
            self.config.FROM['name'], self.config.FROM['address']))
        self.logger.info('Subject: {}'.format(self.message_subject))
        self.logger.info('Message: ')
        self.logger.info(message)

        self.logger.info('***************************************')
