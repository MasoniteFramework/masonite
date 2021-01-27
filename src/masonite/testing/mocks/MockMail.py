from ...drivers.mail.Mailable import Mailable
from ...drivers.mail.BaseMailDriver import BaseMailDriver


class MailableAssertions():

    def hasTo(self, to):
        assert to in self._to
        return self

    def hasSubject(self, subject):
        assert subject == self._subject
        return self

    def hasReplyTo(self, reply_to):
        assert reply_to in self._reply_to
        return self

    def isSentFrom(self, sent_from):
        assert sent_from == self._from
        return self

    def hasView(self, template):
        assert template == self.template
        return self

    def hasInContext(self, key, val=None):
        assert key in self.variables
        if val:
            assert self.variables[key] == val
        return self

    def hasContext(self, context):
        assert context == self.variables
        return self

    @classmethod
    def patch(cls, target):
        for k in cls.__dict__:
            obj = getattr(cls, k)
            if not k.startswith('_') and callable(obj):
                setattr(target, k, obj)


class MockMail(BaseMailDriver):

    def __init__(self, container):
        super().__init__(container)
        self.mails = []

    def send(self, message=None):
        if self._mailable:
            # attach mailable tests helpers
            MailableAssertions.patch(self._mailable.__class__)
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

    def assertSent(self, mailable_class, test_method=None, count=1):
        # if not issubclass(mailable_class, Mailable):
        #     raise ValueError("assertSent accepts only Mailable class")
        sent_mails = [mail['mailable'] for mail in self.mails if (mail["mailable"] and mail["mailable"].__class__ == mailable_class)]
        assert count == len(sent_mails)
        if test_method:
            assert test_method(sent_mails[0])

    def assertSentTo(self, recipients, mailable):
        pass

    def assertNotSentTo(self, recipients, mailable):
        pass