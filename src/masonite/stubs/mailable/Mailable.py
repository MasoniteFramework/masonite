from masonite.mail import Mailable


class __class__(Mailable):
    def build(self):
        return (
            self.to("user@gmail.com")
            .subject("Masonite 4")
            .from_("admin@gmail.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )
