from ...drivers.mail.BaseMailDriver import BaseMailDriver


class MockMail(BaseMailDriver):

    def __init__(self, container):
        super().__init__(container)
        self.mails = []

    def send(self, message=None):
        self.mails.append(message)

    def driver(self, driver):
        return self

    def assertCount(self, count):
        import pdb ; pdb.set_trace()
        assert len(self.mails) == count

    def assertNothingSent(self):
        assert not self.mails

    def assertSentTo(self, recipients, mailable):
        pass

    def assertNotSentTo(self, recipients, mailable):
        pass