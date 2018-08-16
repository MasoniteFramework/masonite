from config import mail
import pytest
import os

from masonite.app import App
from masonite.exceptions import DriverNotFound
from masonite.view import View
from masonite.managers.MailManager import MailManager
from masonite.drivers.MailSmtpDriver import MailSmtpDriver as MailDriver
from masonite.drivers.MailMailgunDriver import MailMailgunDriver as Mailgun



if os.getenv('MAILGUN_SECRET'):

    class UserMock:
        pass

    class TestMailgunDriver:

        def setup_method(self):
            self.app = App()

            self.app.bind('Test', object)
            self.app.bind('MailConfig', mail)
            self.app.bind('MailSmtpDriver', MailDriver)
            self.app.bind('MailMailgunDriver', Mailgun)
            self.app.bind('View', View(self.app))

        def test_mailgun_driver(self):
            user = UserMock
            user.email = 'test@email.com'

            assert MailManager(self.app).driver('mailgun').to(user).to_address == 'test@email.com'


        def test_mail_renders_template(self):

            assert 'MasoniteTesting' in MailManager(self.app).driver('mailgun').to(
                'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body
