from tests.core.test_mail_log_drivers import UserMock
from src.masonite.testing import TestCase
from src.masonite.drivers.mail.BaseMailDriver import BaseMailDriver as Mail


class TestUnitTest(TestCase):

    def setUp(self):
        super().setUp()
        self.mail = Mail.fake()

    def tearDown(self):
        super().tearDown()
        self.mail = Mail.restore()

    def test_mocking_mailgun(self):
        self.mail.driver('mailgun').to('user@example.com').html('<div>Hello</div>').send()
        self.mail.assertCount(1)

    def test_mocking_log(self):
        user = UserMock
        user.email = 'test@email.com'
        self.mail.assertNothingSent()
        self.mail.driver('log').to(user).reply_to('reply-to@email.com').send('Masonite')
        self.mail.driver('log').to(user).reply_to('reply-to@email.com').send('Masonite')
        self.mail.driver('log').to(user).reply_to('reply-to@email.com').send('Masonite')
        self.mail.assertCount(3)
