"""Verify Email Module."""

import time

import pendulum

from ..auth.Sign import Sign


class MustVerifyEmail:
    """Mixin that adds email verification to a User model."""

    def verify_email(self, mail_manager, request):
        from masonite.mail import Mailable
        from masonite.configuration import config

        sign = Sign()
        token = sign.sign("{0}::{1}".format(self.id, time.time()))
        scheme = request.environ.get("wsgi.url_scheme", "http")
        host = request.environ.get("HTTP_HOST", "localhost")
        link = "{0}://{1}/email/verify/{2}".format(scheme, host, token)
        user_name = getattr(self, "name", "")

        class _VerifyEmail(Mailable):
            def build(self):
                return (
                    self.subject("Please Confirm Your Email")
                    .from_(config("mail.from_address"))
                    .view(
                        "auth.mailables.verify_email",
                        {"name": user_name, "link": link},
                    )
                )

        mail_manager.mailable(_VerifyEmail().to(self.email)).send()

    def has_verified_email(self):
        return self.verified_at is not None

    def mark_email_as_verified(self):
        self.verified_at = pendulum.now().to_datetime_string()
        self.save()
