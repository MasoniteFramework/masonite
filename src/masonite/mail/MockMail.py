from .Mail import Mail


class MockMail(Mail):
    def __init__(self, application, *args, **kwargs):
        super().__init__(application, *args, **kwargs)
        self.count = 0

    def send(self, driver=None):
        self.count += 1
        return self

    def seeEmailBcc(self, bcc):
        assert bcc == self.options.get(
            "bcc"
        ), f"BCC of {self.options.get('bcc')} does not match expected {bcc}"
        return self

    def seeEmailCc(self, cc):
        assert cc == self.options.get(
            "cc"
        ), f"CC of {self.options.get('cc')} does not match expected {cc}"
        return self

    def seeEmailContains(self, contents):
        assert contents in self.options.get(
            "html_content"
        ) or contents in self.options.get(
            "text_content"
        ), f"Could not find the {contents} in the email"
        return self

    def getHtmlContents(self, contents):
        return self.options.get("html_content")

    def getTextContents(self, contents):
        return self.options.get("text_content")

    def seeEmailCountEquals(self, count):
        assert (
            count == self.count
        ), f"Email count of {self.count} does not match expected {count}"
        return self

    def seeEmailDoesNotContain(self, contents):
        assert contents not in self.options.get(
            "html_content"
        ) and contents not in self.options.get(
            "text_content"
        ), f"Found {contents} in the email but should not be"
        return self

    def seeEmailFrom(self, assertion):
        assert assertion == self.options.get(
            "from"
        ), f"Assertion of from address {self.options.get('from')} does not match expected {assertion}"
        return self

    def seeEmailReplyTo(self, assertion):
        assert assertion == self.options.get(
            "reply_to"
        ), f"Assertion of reply-to {self.options.get('reply_to')} does not match expected {assertion}"
        return self

    def seeEmailSubjectContains(self, assertion):
        assert assertion in self.options.get(
            "subject"
        ), f"Assertion of subject {self.options.get('subject')} does not contain expected {assertion}"
        return self

    def seeEmailSubjectDoesNotContain(self, assertion):
        assert assertion not in self.options.get(
            "subject"
        ), f"Assertion of subject {self.options.get('subject')} does contain expected {assertion}"
        return self

    def seeEmailSubjectEquals(self, assertion):
        assert assertion == self.options.get(
            "subject"
        ), f"Assertion of subject address {self.options.get('subject')} does not match expected {assertion}"
        return self

    def seeEmailTo(self, assertion):
        assert assertion == self.options.get(
            "to"
        ), f"Assertion of to address {self.options.get('to')} does not match expected {assertion}"
        return self

    def seeEmailPriority(self, assertion):
        assert assertion == self.options.get(
            "priority"
        ), f"Assertion of priority {self.options.get('priority')} does not match expected {assertion}"
        return self

    def seeEmailWasNotSent(self):
        assert self.count == 0, "Expected email was not sent but it was sent"
        return self

    def seeEmailWasSent(self):
        assert self.count > 0, "Expected email was not sent but it was sent"
        return self
