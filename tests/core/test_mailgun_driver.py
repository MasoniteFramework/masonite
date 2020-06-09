import os
import unittest

from src.masonite import env
from src.masonite.app import App
from src.masonite.drivers import MailMailgunDriver as Mailgun
from src.masonite.environment import LoadEnvironment
from src.masonite.managers.MailManager import MailManager
from src.masonite.view import View

LoadEnvironment()


class MailgunTestDriver(Mailgun):
    def _send_mail(self, data):
        return data


if os.getenv('MAILGUN_SECRET'):

    class UserMock:
        pass

    class TestMailgunDriver(unittest.TestCase):

        def setUp(self):
            self.app = App()
            self.app.bind('Container', self.app)
            self.app.bind('Test', object)
            self.app.bind('MailMailgunDriver', MailgunTestDriver)
            viewClass = View(self.app)
            self.app.bind('ViewClass', viewClass)
            self.app.bind('View', viewClass.render)

        def test_mailgun_driver(self):
            user = UserMock
            user.email = 'test@email.com'

            self.assertEqual(MailManager(self.app).driver('mailgun').to(user).to_addresses, ['test@email.com'])
            self.assertEqual(MailManager(self.app).driver('mailgun').reply_to('reply_to@email.com').message_reply_to , 'reply_to@email.com')

        def test_mail_renders_template(self):
            self.assertIn('MasoniteTesting', MailManager(self.app).driver('mailgun').to(
                'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body)

        def test_html_together_with_text_content(self):
            data = MailManager(self.app).driver('mailgun').to('user@example.com').html('<div>Hello</div>').text('hello').send()
            self.assertEqual(data['text'], 'hello')
            self.assertEqual(data['html'], '<div>Hello</div>')

        def test_html_content_only(self):
            data = MailManager(self.app).driver('mailgun').to('user@example.com').html('<div>Hello</div>').send()
            self.assertNotIn('text', data)
            self.assertEqual(data['html'], '<div>Hello</div>')

        def test_text_content_only(self):
            data = MailManager(self.app).driver('mailgun').to('user@example.com').text('hello').send()
            self.assertNotIn('html', data)
            self.assertEqual(data['text'], 'hello')

        def test_passing_message_to_send(self):
            data = MailManager(self.app).driver('mailgun').to('user@example.com').text('hello').html('<div>hello</div>').send('Foo')
            self.assertNotIn('text', data)
            self.assertEqual(data['html'], 'Foo')

        def test_modified_message(self):
            mail = MailManager(self.app).driver('mailgun').to('user@example.com').text('test text')
            data = mail.message()
            data['o:tag'] = ['Foo', 'Bar']
            data = mail.send(data)
            self.assertEqual(data['o:tag'], ['Foo', 'Bar'])

        def test_custom_message(self):
            data = {
                'from': 'other@example.com',
                'to': 'brother@example.com',
                'subject': 'Custom Message',
                'text': 'Custom Text',
            }
            self.assertEqual(MailManager(self.app).driver('mailgun').to('user@example.com').text('test text').send(data), data)

        def _assert_deprecated_send_method(self, data, warning):
            self.assertEqual(data['html'], '<div>Foo</div>')
            self.assertNotIn('text', data)
            self.assertEqual(warning.warnings[0].message.args[0],
                             'Passing message to .send() is a deprecated. Please use .text() and .html().')

        def test_deprecated_send_method_using_positional_arg(self):
            with self.assertWarns(DeprecationWarning) as dw:
                mail = MailManager(self.app).driver('mailgun')
                data = mail.to('user@example.com').text('My Text').html('My HTML').send('<div>Foo</div>')
                self._assert_deprecated_send_method(data, dw)

        def test_deprecated_send_method_using_named_arg(self):
            with self.assertWarns(DeprecationWarning) as dw:
                mail = MailManager(self.app).driver('mailgun')
                data = mail.to('user@example.com').text('My Text').html('My HTML').send(message='<div>Foo</div>')
                self._assert_deprecated_send_method(data, dw)

        def test_mail_sends_with_queue_and_without_queue(self):
            if env('RUN_MAIL'):
                self.assertEqual(MailManager(self.app).driver('mailgun').to('idmann509@gmail.com').send('test queue'), None)
                self.assertEqual(MailManager(self.app).driver('mailgun').queue().to('idmann509@gmail.com').send('test queue'), None)
