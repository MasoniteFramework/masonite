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

class MailWithAsserts():

    def __init__(self, obj, mailable=None):
        self.mailable = obj._mailable
        if self.mailable:
            # TODO: do this ?
            MailableAssertions.patch(self.mailable.__class__)
            self.context = self.mailable.variables
            self.view = self.mailable.template
            self.to = self.mailable._to
            self.sent_from = self.mailable._from
            self.reply_to = self.mailable._reply_to
            self.subject = self.mailable._subject
        else:
            self.context = obj._template_context
            self.view = obj._template_name
            self.to = obj.to_addresses
            # TODO: check from name and address ? for mailable ?
            self.sent_from = obj.from_name
            self.reply_to = obj.message_reply_to
            self.subject = obj.message_subject
        self.html_content = obj.html_content or ""
        self.text_content = obj.text_content or ""

    def hasTo(self, to):
        assert to in self.to
        return self

    def hasSubject(self, subject):
        assert subject == self.subject
        return self

    def hasReplyTo(self, reply_to):
        assert reply_to in self.reply_to
        return self

    def isSentFrom(self, sent_from):
        assert sent_from == self.sent_from
        return self

    def hasView(self, view):
        assert view == self.view
        return self

    def hasInContext(self, key, val=None):
        assert key in self.context
        if val:
            assert self.context[key] == val
        return self

    def hasContext(self, context):
        assert context == self.context
        return self

    def seeInHtml(self, data):
        assert data in self.html_content
        return self

    def seeInText(self, data):
        assert data in self.text_content
        return self

    def seeIn(self, data):
        assert data in self.text_content or data in self.html_content
        return self

    def _isMailable(self, mailable_class):
        return self.mailable and self.mailable.__class__ == mailable_class


class MockMail(BaseMailDriver):

    def __init__(self, container):
        super().__init__(container)
        self.mails = []

    def send(self, message=None):
        """Mock sending email."""
        if self._mailable:
            # attach mailable tests helpers
            MailableAssertions.patch(self._mailable.__class__)
        mail = MailWithAsserts(self)
        self.mails.append(mail)

    def driver(self, driver):
        return self

    def assertCountAll(self, count):
        assert len(self.mails) == count

    def assertNothingSent(self):
        assert not self.mails

    def assertSent(self, mailable_class, test_method=None, count=1):
        # if not issubclass(mailable_class, Mailable):
        #     raise ValueError("assertSent accepts only Mailable class")
        sent_mails = [mail for mail in self.mails if mail._isMailable(mailable_class)]
        assert count == len(sent_mails)
        if test_method:
            assert test_method(sent_mails[0].mailable)

    def assertSentTo(self, recipients, mailable_class):
        if not isinstance(recipients, list):
            recipients = [recipients]
        sent_mails = []
        for recipient in recipients:
            sent_mails += [mail for mail in self.mails if mail._isMailable(mailable_class) and mail.hasTo(recipient)]
        assert len(sent_mails) == len(recipients)
        return sent_mails

    def assertNotSentTo(self, recipients, mailable_class):
        # TODO: should this fail for every of the recipient ?
        sent_mails = self.assertSentTo(recipients, mailable_class)
        assert len(sent_mails) != len(recipients)

    def assertLast(self):
        assert len(self.mails) > 0
        return self.mails[-1]
