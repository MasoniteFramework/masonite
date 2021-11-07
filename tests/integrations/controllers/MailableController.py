from src.masonite.controllers import Controller
from src.masonite.views import View
from src.masonite.mail import Mailable, Mail


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )


class MailableController(Controller):
    def view(self, mail: Mail):
        mail.mailable(Welcome()).send(driver="mailgun")
