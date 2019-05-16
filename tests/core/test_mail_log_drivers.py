from config import mail
 
import os

from masonite.app import App
from masonite.view import View
from masonite.managers.MailManager import MailManager
from masonite.drivers import MailLogDriver
from masonite.drivers import MailTerminalDriver
import unittest
import sys
from contextlib import contextmanager
from _io import StringIO

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class UserMock:
    pass

class TestMailLogDrivers(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app = self.app.bind('Container', self.app)

        self.app.bind('Test', object)
        self.app.bind('MailConfig', mail)
        self.app.bind('View', View(self.app))
        self.app.bind('MailLogDriver', MailLogDriver)
        self.app.bind('MailTerminalDriver', MailTerminalDriver)

    def test_log_driver(self):
        user = UserMock
        user.email = 'test@email.com'

        self.assertEqual(MailManager(self.app).driver('log').to(user).to_address, 'test@email.com')

    def test_log_mail_renders_template(self):

        self.assertIn('MasoniteTesting', MailManager(self.app).driver('log').to(
            'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body)

    def test_terminal_driver(self):
        user = UserMock
        user.email = 'test@email.com'

        self.assertEqual(MailManager(self.app).driver('terminal').to(user).to_address, 'test@email.com')

    def test_terminal_mail_renders_template(self):

        self.assertIn('MasoniteTesting', MailManager(self.app).driver('terminal').to(
            'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body)

    def test_log_driver_output(self):
        user = UserMock
        user.email = 'test@email.com'

        MailManager(self.app).driver('log').to(user).send('Masonite')

        filepath = '{0}/{1}'.format('bootstrap/mail', 'mail.log')
        self.logfile = open(filepath, 'r')
        file_string = self.logfile.read()

        self.assertIn('test@email.com', file_string)

    def test_terminal_driver_output(self):
        user = UserMock
        user.email = 'test@email.com'
        with captured_output() as (out, err):
            MailManager(self.app).driver('terminal').to(user).send('Masonite')

        # This can go inside or outside the `with` block
        error = err.getvalue().strip()
        self.assertIn('test@email.com', error)

    def tearDown(self):
        if hasattr(self, 'logfile') and self.logfile:
            self.logfile.close()

        filepath = '{0}/{1}'.format('bootstrap/mail', 'mail.log')
        if os.path.isfile(filepath):
            os.remove(filepath)
