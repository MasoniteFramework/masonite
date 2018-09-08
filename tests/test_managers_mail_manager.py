from config import mail as mail_config
import pytest

from masonite.app import App
from masonite.exceptions import DriverNotFound
from masonite.managers import MailManager
from masonite.drivers import MailSmtpDriver as MailDriver
from masonite.drivers import MailMailgunDriver as Mailgun
from masonite.contracts import MailManagerContract
from masonite.view import View
from masonite.contracts import MailContract


class MailSmtpDriver:

    def __init__(self, Test=None):
        self.test = Test

    def send(self, message):
        return message
    
class User:
    pass

class TestMailManager:

    def setup_method(self):
        self.app = App()
        self.app = self.app.bind('Container', self.app)

        self.app.bind('Test', object)
        self.app.bind('MailSmtpDriver', object)
        self.app.bind('MailConfig', mail_config)
        self.app.bind('View', View(self.app))

    def test_mail_manager_loads_container(self):
        mailManager = MailManager()
        assert mailManager.load_container(self.app) 

    def test_mail_manager_resolves_from_contract(self):
        self.app.bind('MailManager', MailManager())
        assert self.app.resolve(self._test_resolve) == self.app.make('MailManager')
    
    def _test_resolve(self, mail: MailManagerContract):
        return mail

    def test_creates_driver(self):
        mailManager = MailManager()

        assert mailManager.load_container(self.app).manage_driver == object

    def test_does_not_create_driver_with_initilization_container(self):

        mailManager = MailManager(self.app)

        assert mailManager.manage_driver == None

    def test_does_not_raise_drivernotfound_exception(self):

        mailManager = MailManager(self.app)

    def test_manager_sets_driver(self):
        self.app.bind('MailMailtrapDriver', Mailgun)

        mailManager = MailManager(self.app).driver('mailtrap')

    def test_manager_sets_driver_throws_driver_not_found_exception(self):
        with pytest.raises(DriverNotFound, message="Should raise DriverNotFound error"):
            mailManager = MailManager(self.app).driver('mailtrap')

    def test_drivers_are_resolvable_by_container(self):
        self.app.bind('MailSmtpDriver', MailDriver)

        assert isinstance(MailManager(self.app).driver('smtp'), MailDriver)

    def test_send_mail(self):
        self.app.bind('MailSmtpDriver', MailDriver)
        assert MailManager(self.app).driver('smtp').to('idmann509@gmail.com')

    def test_send_mail_with_from(self):
        self.app.bind('MailSmtpDriver', MailDriver)

        assert MailManager(self.app).driver('smtp').to('idmann509@gmail.com').send_from('masonite@masonite.com').from_address == 'masonite@masonite.com'

    def test_send_mail_with_subject(self):
        self.app.bind('MailSmtpDriver', MailDriver)

        assert MailManager(self.app).driver('smtp').to('').subject('test').message_subject == 'test'

    def test_send_mail_with_callable(self):
        self.app.bind('MailSmtpDriver', MailDriver)
        user = User
        user.email = 'email@email.com'
        assert MailManager(self.app).driver('smtp').to(User)

    def test_switch_mail_manager(self):
        self.app.bind('MailSmtpDriver', MailDriver)
        self.app.bind('MailTestDriver', Mailgun)

        mail_driver = MailManager(self.app).driver('smtp')

        assert isinstance(mail_driver.driver('test'), Mailgun)
    
    def test_mail_helper_method_resolves_a_driver(self):
        print(mail())
        assert isinstance(mail(), MailContract)
