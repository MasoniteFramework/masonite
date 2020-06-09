from email.mime.multipart import MIMEMultipart

from src.masonite import env
from src.masonite.app import App
from src.masonite.drivers import MailMailgunDriver as Mailgun, Mailable
from src.masonite.drivers import MailSmtpDriver
from src.masonite.environment import LoadEnvironment
from src.masonite.managers.MailManager import MailManager
from src.masonite.view import View
import unittest
from src.masonite.testing import TestCase

LoadEnvironment()


class UserMock:
    pass


class MailSmtpTestDriver(MailSmtpDriver):
    def _send_mail(self, mail_from_header, to_addresses, message):
        return mail_from_header, to_addresses, message.as_string()

    def _smtp_connect(self):
        pass


text_content = 'Hi MasoniteTextTesting\nWelcome to MasoniteFramework!'
html_content = '<div class="title m-b-md">MasoniteHTMLTesting</div>'


class TestSMTPDriver(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Container', self.app)

        self.app.bind('Test', object)
        self.app.bind('MailSmtpDriver', MailSmtpTestDriver)
        viewClass = View(self.app)
        self.app.bind('ViewClass', viewClass)
        self.app.bind('View', viewClass.render)

    def test_smtp_driver(self):
        user = UserMock
        user.email = 'test@email.com'

        self.assertEqual(MailManager(self.app).driver('smtp').to(user).to_addresses, ['test@email.com'])
        self.assertEqual(MailManager(self.app).driver('smtp').reply_to('reply_to@email.com').message_reply_to , 'reply_to@email.com')

    def test_mail_text_content(self):
        mail = MailManager(self.app).driver('smtp').to('idmann509@gmail.com').text(text_content)
        self.assertEqual(mail.text_content, text_content)
        self.assertEqual(mail.message_body, text_content)
        self.assertEqual(mail.html_content, None)
        _, _, message_as_string = mail.send()
        self.assertIn('Content-Type: text/plain', message_as_string)
        self.assertNotIn('Content-Type: text/html', message_as_string)

    def test_mail_html_content(self):
        mail = MailManager(self.app).driver('smtp').to('idmann509@gmail.com').html(html_content)
        self.assertEqual(html_content, mail.html_content)
        self.assertEqual(mail.message_body, mail.html_content)
        self.assertEqual(mail.text_content, None)
        _, _, message_as_string = mail.send()
        self.assertIn('Content-Type: text/html', message_as_string)
        self.assertNotIn('Content-Type: text/plain', message_as_string)

    def test_mail_text_and_html_content(self):
        mail = MailManager(self.app).driver('smtp').to('idmann509@gmail.com').text(text_content).html(html_content)
        self.assertIn(html_content, mail.html_content)
        self.assertEqual(mail.message_body, mail.html_content)
        self.assertEqual(mail.text_content, text_content)
        _, _, message_as_string = mail.send()
        self.assertIn('Content-Type: text/plain', message_as_string)
        self.assertIn('Content-Type: text/html', message_as_string)

    def test_modified_message(self):
        mail = MailManager(self.app).driver('smtp').to('idmann509@gmail.com').text(text_content).html(html_content)
        message = mail.message()
        message['Bcc'] = 'cc@example.com'
        _, _, message_as_string = mail.send(message)
        self.assertIn('Bcc: cc@example.com\n', message_as_string)

    def test_custom_message(self):
        mail = MailManager(self.app).driver('smtp')
        message = MIMEMultipart('alternative')
        message['From'] = 'a@example.com'
        message['Cc'] = 'b@example.com'
        message.add_header('X-My-Custom-Header', 'my custom value')
        _, _, message_as_string = mail.to('user@example.com').text('test text').send(message)
        self.assertIn('From: a@example.com\n', message_as_string)
        self.assertIn('Cc: b@example.com\n', message_as_string)
        self.assertIn('X-My-Custom-Header: my custom value\n', message_as_string)
        self.assertNotIn('Subject:', message_as_string)
        self.assertNotIn('test text', message_as_string)

    def _assert_deprecated_send_method(self, message_as_string, warning):
        self.assertIn('<div>Foo</div>', message_as_string)
        self.assertNotIn('My Text', message_as_string)
        self.assertNotIn('My HTML', message_as_string)
        self.assertIn('Content-Type: text/html', message_as_string)
        self.assertNotIn('Content-Type: text/plain', message_as_string)
        self.assertEqual(warning.warnings[0].message.args[0],
                         'Passing message_contents to .send() is a deprecated. Please use .text() and .html().')

    def test_deprecated_send_method_using_positional_arg(self):
        with self.assertWarns(DeprecationWarning) as dw:
            mail = MailManager(self.app).driver('smtp')
            _, _, message_as_string = mail.to('user@example.com').text('My Text').html('My HTML').send('<div>Foo</div>')
            self._assert_deprecated_send_method(message_as_string, dw)

    def test_deprecated_send_method_using_named_arg(self):
        with self.assertWarns(DeprecationWarning) as dw:
            mail = MailManager(self.app).driver('smtp')
            _, _, message_as_string = mail.to('user@example.com').text('My Text').html('My HTML').send(message_contents='<div>Foo</div>')
            self._assert_deprecated_send_method(message_as_string, dw)

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
        self.assertEqual(mailable.to_addresses, ['idmann509@gmail.com'])
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
    

