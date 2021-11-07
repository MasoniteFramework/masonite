from src.masonite.notification import Notification, Textable
from src.masonite.mail import Mailable
from src.masonite.mail import Mailable


class OneTimePassword(Notification, Mailable, Textable):
    def to_mail(self, notifiable):
        return (
            self.to(notifiable.email)
            .subject("Masonite 4")
            .from_("hello@email.com")
            .text(f"Hello {notifiable.name}")
        )

    def to_vonage(self, notifiable):
        return self.text_message("Welcome !").to("6314870798").from_("33123456789")

    def via(self, notifiable):
        return ["vonage"]
