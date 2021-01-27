from ...drivers.mail.Mailable import Mailable
from ...drivers.mail.BaseMailDriver import BaseMailDriver


class MockMail(BaseMailDriver):

    def __init__(self, container):
        super().__init__(container)
        self.mails = []

    def send(self, message=None):
        data = {
            "message": message or self.message_body,
            "subject": self.message_subject,
            "text": self.text_content,
            "html": self.html_content,
            "to": self.to_addresses,
            "reply_to": self.message_reply_to,
            "from_name": self.from_name,
            "from_address": self.from_address,
            "template": self._template_name,
            "is_mailable": bool(self._mailable),
            "mailable": self._mailable,
            "context": self._template_context
        }
        self.mails.append(data)

    def driver(self, driver):
        return self

    def assertCountAll(self, count):
        assert len(self.mails) == count

    def assertNothingSent(self):
        assert not self.mails

    def assertSent(self, mailable_class, count=1):
        # if not issubclass(mailable_class, Mailable):
        #     raise ValueError("assertSent accepts only Mailable class")
        sent_mails = [mail['mailable'] for mail in self.mails if (mail["mailable"] and mail["mailable"].__class__ == mailable_class)]
        import pdb ; pdb.set_trace()
        assert count == len(sent_mails)

    def assertSentTo(self, recipients, mailable):
        pass

    def assertNotSentTo(self, recipients, mailable):
        pass