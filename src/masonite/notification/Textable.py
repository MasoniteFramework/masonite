from .Sms import Sms


class Textable:
    def text_message(self, message):
        return Sms().text(message)
