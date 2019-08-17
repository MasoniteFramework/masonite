from masonite.environment import LoadEnvironment

LoadEnvironment()

from config import mail
from masonite.app import App
from masonite.contracts import MailManagerContract
from masonite.drivers import MailMailgunDriver as Mailgun
from masonite.drivers import MailSmtpDriver as MailDriver
from masonite.exceptions import DriverNotFound
from masonite.managers import MailManager
from masonite.view import View
from masonite.contracts import MailContract
from masonite import env
import unittest


class MailSmtpDriver:

    def __init__(self, Test=None):
        self.test = Test

    def send(self, message):
        return message


class User:
    pass


class TestMailManager(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app = self.app.bind('Container', self.app)

        self.app.bind('Test', object)
        self.app.bind('MailSmtpDriver', object)
        self.app.bind('MailConfig', mail)
        self.app.bind('View', View(self.app).render)
        self.app.bind('ViewClass', View(self.app))

    def test_mail_manager_loads_container(self):
        mailManager = MailManager(self.app)
        self.assertTrue(mailManager.load_container(self.app))

    def test_mail_manager_resolves_from_contract(self):
        self.app.singleton('MailManager', MailManager)
        self.assertEqual(self.app.resolve(self._test_resolve), self.app.make('MailManager'))

    def _test_resolve(self, mail: MailManagerContract):
        return mail

    def test_creates_driver(self):
        mailManager = MailManager(self.app)

        self.assertIsInstance(mailManager.manage_driver, object)

    def test_does_not_create_driver_with_initilization_container(self):

        mailManager = MailManager(self.app)

        self.assertEqual(mailManager.manage_driver, None)

    def test_does_not_raise_drivernotfound_exception(self):
        MailManager(self.app)

    def test_manager_sets_driver(self):
        self.app.bind('MailMailtrapDriver', Mailgun)
        MailManager(self.app).driver('mailtrap')

    def test_manager_sets_driver_throws_driver_not_found_exception(self):
        with self.assertRaises(DriverNotFound, "Should raise DriverNotFound error"):
            MailManager(self.app).driver('mailtrap')

    def test_drivers_are_resolvable_by_container(self):
        self.app.bind('MailSmtpDriver', MailDriver)

        self.assertIsInstance(MailManager(self.app).driver('smtp'), MailDriver)

    def test_driver_loads_template(self):
        self.app.bind('MailSmtpDriver', MailDriver)

        driver = MailManager(self.app).driver('smtp')

        self.assertEqual(driver.template('test', {'test': 'test'}).message_body, 'test')

    def test_send_mail(self):
        self.app.bind('MailSmtpDriver', MailDriver)
        self.assertTrue(MailManager(self.app).driver('smtp').to('idmann509@gmail.com'))

    def test_send_mail_with_from(self):
        self.app.bind('MailSmtpDriver', MailDriver)

        self.assertEqual(MailManager(self.app).driver('smtp').to('idmann509@gmail.com').send_from('masonite@masonite.com').from_address, 'masonite@masonite.com')

    def test_send_mail_sends(self):
        if env('RUN_MAIL'):
            self.app.bind('MailSmtpDriver', MailDriver)

            self.assertTrue(MailManager(self.app).driver('smtp').to('idmann509@gmail.com').send('hi'))

    def test_send_mail_sends_with_queue(self):
        if env('RUN_MAIL'):
            self.app.bind('MailSmtpDriver', MailDriver)

            self.assertEqual(MailManager(self.app).driver('smtp').to('idmann509@gmail.com').queue().send('hi'), None)

    def test_send_mail_with_subject(self):
        self.app.bind('MailSmtpDriver', MailDriver)

        self.assertEqual(MailManager(self.app).driver('smtp').to('').subject('test').message_subject, 'test')

    def test_send_mail_with_callable(self):
        self.app.bind('MailSmtpDriver', MailDriver)
        user = User
        user.email = 'email@email.com'
        self.assertTrue(MailManager(self.app).driver('smtp').to(User))

    def test_switch_mail_manager(self):
        self.app.bind('MailSmtpDriver', MailDriver)
        self.app.bind('MailTestDriver', Mailgun)

        mail_driver = MailManager(self.app).driver('smtp')

        self.assertIsInstance(mail_driver.driver('test'), Mailgun)

    def test_mail_helper_method_resolves_a_driver(self):
        self.assertIsInstance(mail_helper(), MailContract)
