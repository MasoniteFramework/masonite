""" Verify Email Module """

import time

from masonite.auth.Sign import Sign
from masonite.managers import MailManager
from masonite.request import Request


class MustVerifyEmail:
    """Class To Verify User Email
    """

    def verify_email(self, mail_manager: MailManager, request: Request):
        mail = mail_manager.helper()
        sign = Sign()

        token = sign.sign('{0}::{1}'.format(self.id, time.time()))
        link = '{0}/email/verify/{1}'.format(request.environ['HTTP_HOST'], token)

        mail.to(self.email) \
            .template('auth/verifymail', {'name': self.name, 'email': self.email, 'link': link}) \
            .subject('Please Confirm Your Email').send()
