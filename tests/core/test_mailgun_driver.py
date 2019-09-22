import os

from config import mail
from masonite import env
from masonite.app import App
from masonite.drivers import MailMailgunDriver as Mailgun
from masonite.drivers import MailSmtpDriver as MailDriver
from masonite.environment import LoadEnvironment
from masonite.managers.MailManager import MailManager
from masonite.view import View
import unittest

LoadEnvironment()

if os.getenv('MAILGUN_SECRET'):

    class UserMock:
        pass

    class TestMailgunDriver(unittest.TestCase):

        def setUp(self):
            self.app = App()
            self.app.bind('Container', self.app)

            self.app.bind('Test', object)
            self.app.bind('MailConfig', mail)
            self.app.bind('MailSmtpDriver', MailDriver)
            self.app.bind('MailMailgunDriver', Mailgun)
            viewClass = View(self.app)
            self.app.bind('ViewClass', viewClass)
            self.app.bind('View', viewClass.render)

        def test_mailgun_driver(self):
            user = UserMock
            user.email = 'test@email.com'

            self.assertEqual(MailManager(self.app).driver('mailgun').to(user).to_address, 'test@email.com')
            self.assertEqual(MailManager(self.app).driver('mailgun').reply_to('reply_to@email.com').message_reply_to , 'reply_to@email.com')

        def test_mail_renders_template(self):
            self.assertIn('MasoniteTesting', MailManager(self.app).driver('mailgun').to(
                'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body)

        def test_mail_sends_with_queue_and_without_queue(self):
            if env('RUN_MAIL'):
                self.assertEqual(MailManager(self.app).driver('mailgun').to('idmann509@gmail.com').send('test queue'), None)
                self.assertEqual(MailManager(self.app).driver('mailgun').queue().to('idmann509@gmail.com').send('test queue'), None)
