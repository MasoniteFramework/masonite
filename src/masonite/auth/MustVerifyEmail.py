"""Verify Email Module."""

import time

from ..auth.Sign import Sign


class MustVerifyEmail:
    """Class To Verify User Email."""

    def verify_email(self, mail_manager, request):
        """Sends email for user verification

        Arguments:
            mail_manager {masonite.managers.MailManager} -- Masonite mail manager class.
            request {masonite.request.Request} -- Masonite request class.
        """
        mail = mail_manager.helper()
        sign = Sign()

        token = sign.sign("{0}::{1}".format(self.id, time.time()))
        link = "{0}/email/verify/{1}".format(request.environ["HTTP_HOST"], token)

        mail.to(self.email).template(
            "auth/verifymail", {"name": self.name, "email": self.email, "link": link}
        ).subject("Please Confirm Your Email").send()
