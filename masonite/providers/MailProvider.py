"""A Mail Service Provider."""

from masonite.drivers import MailMailgunDriver, MailSmtpDriver, \
    MailLogDriver, MailTerminalDriver
from masonite.managers import MailManager
from masonite.provider import ServiceProvider
from masonite import Mail


class MailProvider(ServiceProvider):

    wsgi = False

    def register(self):
        from config import mail
        self.app.bind('MailConfig', mail)
        self.app.bind('MailSmtpDriver', MailSmtpDriver)
        self.app.bind('MailMailgunDriver', MailMailgunDriver)
        self.app.bind('MailLogDriver', MailLogDriver)
        self.app.bind('MailTerminalDriver', MailTerminalDriver)
        self.app.bind('MailManager', MailManager(self.app))

    def boot(self, manager: MailManager):
        self.app.bind('Mail', manager.driver(self.app.make('MailConfig').DRIVER))
        self.app.swap(Mail, manager.driver(self.app.make('MailConfig').DRIVER))
