from src.masonite import env
from src.masonite.app import App
from src.masonite.drivers import MailMailgunDriver as Mailgun, Mailable
from src.masonite.drivers import MailSmtpDriver as MailDriver
from src.masonite.environment import LoadEnvironment
from src.masonite.managers.MailManager import MailManager
from src.masonite.view import View
import unittest
from masonite.testing import TestCase

LoadEnvironment()


class UserMock:
    pass


class TestSMTPDriver(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Container', self.app)

        self.app.bind('Test', object)
        self.app.bind('MailSmtpDriver', MailDriver)
        self.app.bind('MailMailgunDriver', Mailgun)
        viewClass = View(self.app)
        self.app.bind('ViewClass', viewClass)
        self.app.bind('View', viewClass.render)

    def test_smtp_driver(self):
        user = UserMock
        user.email = 'test@email.com'

        self.assertEqual(MailManager(self.app).driver('smtp').to(user).to_address, 'test@email.com')
        self.assertEqual(MailManager(self.app).driver('smtp').reply_to('reply_to@email.com').message_reply_to , 'reply_to@email.com')

    def test_mail_renders_template(self):
        self.assertIn('MasoniteTesting', MailManager(self.app).driver('smtp').to(
            'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body)

    def test_mail_sends_with_queue_and_without_queue(self):
        if env('RUN_MAIL'):
            self.assertEqual(MailManager(self.app).driver('smtp').to('idmann509@gmail.com').send('test queue'), None)
            self.assertEqual(MailManager(self.app).driver('smtp').queue().to('idmann509@gmail.com').send('test queue'), None)

class TestMailable(TestCase):

    def setUp(self):
        super().setUp()
        pass

    def test_works(self):
        mailable = MailManager(self.container).driver('smtp').mailable(ForgotPasswordMailable())
        self.assertEqual(mailable.to_address, 'idmann509@gmail.com')
        self.assertEqual(mailable.from_address, 'admin@test.com')
        self.assertEqual(mailable.message_subject, 'Forgot Password')
        self.assertEqual(mailable.message_body, 'testing email')
        self.assertEqual(mailable.message_reply_to, 'customer@email.com')
        self.assertTrue(True)

class ForgotPasswordMailable(Mailable):

    def build(self):
        return (self
            .to('idmann509@gmail.com')
            .send_from('admin@test.com')
            .view('emails.test')
            .reply_to('customer@email.com')
            .subject('Forgot Password'))
    

