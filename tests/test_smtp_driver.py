from config import mail
import pytest

from masonite.app import App
from masonite.exceptions import DriverNotFound
from masonite.managers.MailManager import MailManager
from masonite.drivers.MailSmtpDriver import MailSmtpDriver as MailDriver
from masonite.drivers.MailMailgunDriver import MailMailgunDriver as Mailgun


class User:
    pass


def test_mailgun_driver():
    app = App()

    app.bind('Test', object)
    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)
    app.bind('MailMailgunDriver', Mailgun)
    user = User
    user.email = 'idmann509@gmail.com'

    assert MailManager(app).driver('smtp').to(
        user).to_address == 'idmann509@gmail.com'
    assert MailManager(app).driver('smtp').to(user).template(
        'mail/welcome', {'to': 'MasoniteTesting'}).send() is None


def test_mail_renders_template():
    app = App()

    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)

    assert 'MasoniteTesting' in MailManager(app).driver('smtp').to(
        'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body
