from config import mail
import pytest

from masonite.app import App
from masonite.exceptions import DriverNotFound
from masonite.managers.MailManager import MailManager
from masonite.drivers.MailSmtpDriver import MailSmtpDriver as MailDriver
from masonite.drivers.MailMailgunDriver import MailMailgunDriver as Mailgun


def test_mail_renders_template():
    app = App()

    app.bind('MailConfig', mail)
    app.bind('MailSmtpDriver', MailDriver)

    assert 'MasoniteTesting' in MailManager(app).driver('smtp').to(
        'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body
