"""A Mail Service Provider."""

from ..drivers import MailMailgunDriver, MailSmtpDriver, \
    MailLogDriver, MailTerminalDriver
from ..managers import MailManager
from ..provider import ServiceProvider
from .. import Mail
from ..helpers import config


class MailProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('MailSmtpDriver', MailSmtpDriver)
        self.app.bind('MailMailgunDriver', MailMailgunDriver)
        self.app.bind('MailLogDriver', MailLogDriver)
        self.app.bind('MailTerminalDriver', MailTerminalDriver)
        self.app.bind('MailManager', MailManager(self.app))

    def boot(self, manager: MailManager):
        self.app.bind('Mail', manager.driver(config('mail.driver')))
        self.app.swap(Mail, manager.driver(config('mail.driver')))
