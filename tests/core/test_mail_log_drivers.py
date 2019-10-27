from config import mail

import os

from src.masonite.app import App
from src.masonite.view import View
from src.masonite.managers.MailManager import MailManager
from src.masonite.drivers import MailLogDriver
from src.masonite.drivers import MailTerminalDriver
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
        viewClass = View(self.app)
        self.app.bind('ViewClass', viewClass)
        self.app.bind('View', viewClass.render)
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

        MailManager(self.app).driver('log').to(user).reply_to('reply-to@email.com').send('Masonite')

        filepath = '{0}/{1}'.format('bootstrap/mail', 'mail.log')
        self.logfile = open(filepath, 'r')
        file_string = self.logfile.read()

        self.assertIn('test@email.com', file_string)
        self.assertIn('reply-to@email.com', file_string)

    def test_terminal_driver_output(self):
        user = UserMock
        user.email = 'test@email.com'
        with captured_output() as (_, err):
            MailManager(self.app).driver('terminal').to(user).reply_to('reply-to@email.com').send('Masonite')

        # This can go inside or outside the `with` block
        error = err.getvalue().strip()
        self.assertIn('test@email.com', error)
        self.assertIn('reply-to@email.com', error)

    def tearDown(self):
        if hasattr(self, 'logfile') and self.logfile:
            self.logfile.close()

        filepath = '{0}/{1}'.format('bootstrap/mail', 'mail.log')
        if os.path.isfile(filepath):
            os.remove(filepath)
