from masonite.app import App
from config import mail
import pytest
from masonite.exceptions import DriverNotFound
from masonite.managers.MailManager import MailManager
from masonite.drivers.MailSmtpDriver import MailSmtpDriver as MailDriver
from masonite.drivers.MailMailgunDriver import MailMailgunDriver as Mailgun

class MailSmtpDriver(object):

    def __init__(self, Test=None):
        self.test = Test

    def send(self, message):
        return message

def test_mail_manager_loads_container():
    app = App()

    app.bind('Test', object)
    app.bind('MailSmtpDriver', object)
    app.bind('MailConfig', mail)

    mailManager = MailManager()

    assert mailManager.load_container(app) #.container.providers == {'Test': object}

class User(object):
    pass

def test_creates_driver():
    app = App()

    app.bind('Test', object)
    app.bind('MailSmtpDriver', object)
    app.bind('MailConfig', mail)

    mailManager = MailManager()

    assert mailManager.load_container(app).manage_driver == object

def test_creates_driver_with_initilization_container():
    app = App()

    app.bind('Test', object)
    app.bind('MailSmtpDriver', object)
    app.bind('MailConfig', mail)

    mailManager = MailManager(app)

    assert mailManager.manage_driver == object

def test_throws_drivernotfound_exception():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)

    with pytest.raises(DriverNotFound, message="Should raise DriverNotFound error"):
        mailManager = MailManager(app)

def test_manager_sets_driver():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', object)
    app.bind('MailMailtrapDriver', object)

    mailManager = MailManager(app).driver('mailtrap')


def test_manager_sets_driver_throws_driver_not_found_exception():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', object)

    with pytest.raises(DriverNotFound, message="Should raise DriverNotFound error"):
        mailManager = MailManager(app).driver('mailtrap')

def test_driver_sends_mail():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailSmtpDriver)

    # assert MailManager(app).driver('smtp').send('mail') is 'mail'
    # assert MailManager(app).driver('smtp').send('mai') is not 'mail'

def test_drivers_are_resolvable_by_container():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailSmtpDriver)
    app.bind('Test', 'test')

    assert MailManager(app).driver('smtp').test is 'test'
    assert MailManager(app).driver('smtp').test is not 'tet'

def test_send_mail():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)

    assert MailManager(app).driver('smtp').to('idmann509@gmail.com')

def test_send_mail_with_from():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)

    assert MailManager(app).driver('smtp').to('idmann509@gmail.com').send_from('masonite@masonite.com').from_address == 'masonite@masonite.com'

def test_send_mail_with_subject():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)

    assert MailManager(app).driver('smtp').to('').subject('test').message_subject == 'test'

def test_send_mail_with_callable():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)
    user = User
    setattr(user, 'email', 'idmann509@gmail.com')

    assert MailManager(app).driver('smtp').to(User)

def test_mailgun_driver():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)
    app.bind('MailMailgunDriver', Mailgun)
    user = User
    setattr(user, 'email', '')

    assert MailManager(app).driver('mailgun').to(User)

def test_mail_renders_template():
    app = App()

    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)

    assert MailManager(app).driver('smtp').to('idmann509@gmail.com').template('mail/welcome', {'to': 'Masonite'}).send() is None

def test_mailgun_renders_template():
    app = App()

    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)
    app.bind('MailMailgunDriver', Mailgun)

    assert MailManager(app).driver('mailgun').to('idmann509@gmail.com').template('mail/welcome', {'to': 'Masonite'})
