from src.masonite.app import App
from src.masonite.drivers import BaseMailDriver
from src.masonite.environment import LoadEnvironment
from src.masonite.managers.MailManager import MailManager
from src.masonite.view import View
import unittest

LoadEnvironment()


text_content = 'Hi MasoniteTextTesting\nWelcome to MasoniteFramework!'
html_content = '<div class="title m-b-md">MasoniteHTMLTesting</div>'


class MyTestDriver(BaseMailDriver):
    pass


class TestSMTPDriver(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.bind('Container', self.app)
        self.app.bind('MailBaseDriver', MyTestDriver)
        viewClass = View(self.app)
        self.app.bind('ViewClass', viewClass)
        self.app.bind('View', viewClass.render)

    def test_mail_renders_template_with_text_mimetype(self):
        mail = MailManager(self.app).driver('base').to('idmann509@gmail.com').template(
            'mail/welcome.txt', {'to': 'MasoniteTextTesting'}, mimetype='plain')
        self.assertEqual(mail.text_content, text_content)
        self.assertEqual(mail.message_body, mail.text_content)
        self.assertEqual(mail.html_content, None)

    def test_mail_renders_template_with_html_mimetype(self):
        mail = MailManager(self.app).driver('base').to('idmann509@gmail.com').template(
            'mail/welcome.html', {'to': 'MasoniteHTMLTesting'})
        self.assertIn(html_content, mail.html_content)
        self.assertEqual(mail.message_body, mail.html_content)
        self.assertEqual(mail.text_content, None)

    def test_mail_renders_template_with_both_mimetypes(self):
        mail = MailManager(self.app).driver('base').to('idmann509@gmail.com')\
            .template('mail/welcome.html', {'to': 'MasoniteHTMLTesting'}, mimetype='html')\
            .template('mail/welcome.txt', {'to': 'MasoniteTextTesting'}, mimetype='plain')
        self.assertIn(html_content, mail.html_content)
        self.assertEqual(mail.message_body, mail.html_content)
        self.assertEqual(mail.text_content, text_content)
