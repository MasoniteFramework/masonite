from config import mail
import pytest
import os

from masonite.app import App
from masonite.exceptions import DriverNotFound
from masonite.view import View
from masonite.managers.MailManager import MailManager
from masonite.drivers.MailLogDriver import MailLogDriver
from masonite.drivers.MailTerminalDriver import MailTerminalDriver


class UserMock:
    pass

class TestMailLogDrivers:

    def setup_method(self):
        self.app = App()

        self.app.bind('Test', object)
        self.app.bind('MailConfig', mail)
        self.app.bind('MailLogDriver', MailLogDriver)
        self.app.bind('MailTerminalDriver', MailTerminalDriver)
        self.app.bind('View', View(self.app))

    def test_log_driver(self):
        user = UserMock
        user.email = 'test@email.com'

        assert MailManager(self.app).driver('log').to(user).to_address == 'test@email.com'


    def test_log_mail_renders_template(self):

        assert 'MasoniteTesting' in MailManager(self.app).driver('log').to(
            'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body

    def test_terminal_driver(self):
        user = UserMock
        user.email = 'test@email.com'

        assert MailManager(self.app).driver('terminal').to(user).to_address == 'test@email.com'

    def test_terminal_mail_renders_template(self):

        assert 'MasoniteTesting' in MailManager(self.app).driver('terminal').to(
            'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body

    def test_log_driver_output(self):
        user = UserMock
        user.email = 'test@email.com'

        MailManager(self.app).driver('log').to(user).send('Masonite')

        filepath = '{0}/{1}'.format('bootstrap/mail', 'mail.log')
        self.logfile = open(filepath, 'r')
        file_string = self.logfile.read()

        assert 'test@email.com' in file_string

    def test_terminal_driver_output(self, capsys):
        user = UserMock
        user.email = 'test@email.com'

        MailManager(self.app).driver('terminal').to(user).send('Masonite')

        captured = capsys.readouterr()
        assert 'test@email.com' in captured.err

    def teardown_method(self):
        if hasattr(self, 'logfile') and self.logfile:
            self.logfile.close()

        filepath = '{0}/{1}'.format('bootstrap/mail', 'mail.log')
        if os.path.isfile(filepath):
            os.remove(filepath)
