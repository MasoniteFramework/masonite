from .Provider import Provider
from ..mail import Mail
from ..mail.drivers import SMTPDriver, TerminalDriver, MailgunDriver
from ..utils.structures import load
from ..mail import MockMail
from ..facades import Config


class MailProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        mail = Mail(self.application).set_configuration(Config.get("mail.drivers"))
        mail.add_driver("smtp", SMTPDriver(self.application))
        mail.add_driver("mailgun", MailgunDriver(self.application))
        mail.add_driver("terminal", TerminalDriver(self.application))
        self.application.bind("mail", mail)
        self.application.bind("mock.mail", MockMail)

    def boot(self):
        pass
