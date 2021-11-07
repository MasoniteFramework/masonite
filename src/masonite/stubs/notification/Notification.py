from masonite.notification import Notification
from masonite.mail import Mailable


class __class__(Notification, Mailable):
    def to_mail(self, notifiable):
        return (
            self.to(notifiable.email)
            .subject("Masonite 4")
            .from_("hello@email.com")
            .text(f"Hello {notifiable.name}")
        )

    def via(self, notifiable):
        return ["mail"]
