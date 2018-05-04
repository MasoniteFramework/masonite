""" A Mail Service Provider """
from masonite.provider import ServiceProvider
from masonite.drivers.MailSmtpDriver import MailSmtpDriver
from masonite.drivers.MailMailgunDriver import MailMailgunDriver
from masonite.managers.MailManager import MailManager

from config import mail


class MailProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('MailConfig', mail)
        self.app.bind('MailSmtpDriver', MailSmtpDriver)
        self.app.bind('MailMailgunDriver', MailMailgunDriver)
        self.app.bind('MailManager', MailManager(self.app))

    def boot(self, MailConfig, MailManager):
        self.app.bind('Mail', MailManager.driver(MailConfig.DRIVER))
