from typing import TYPE_CHECKING

from .Mail import Mail
from ..configuration import config

if TYPE_CHECKING:
    from ..foundation import Application


class MockMail(Mail):
    def __init__(self, application: "Application", *args, **kwargs):
        super().__init__(application, *args, **kwargs)
        self.count = 0
        self.driver = None

    def reset(self) -> None:
        """Reset mock implementation."""
        self.count = 0
        self.driver = None

    def send(self, driver: str = None) -> "MockMail":
        if driver:
            self.driver = driver
        else:
            self.driver = self.options.get("driver", None) or config(
                "mail.drivers.default"
            )

        config_options = self.get_config_options(self.driver)
        if self.options.get("from"):
            config_options.pop("from", None)
        self.options.update(config_options)
        self.count += 1
        return self

    def seeEmailBcc(self, bcc: str) -> "MockMail":
        assert bcc == self.options.get(
            "bcc"
        ), f"BCC of {self.options.get('bcc')} does not match expected {bcc}"
        return self

    def seeEmailCc(self, cc: str) -> "MockMail":
        assert cc == self.options.get(
            "cc"
        ), f"CC of {self.options.get('cc')} does not match expected {cc}"
        return self

    def seeEmailContains(self, contents: str) -> "MockMail":
        assert contents in self.options.get(
            "html_content"
        ) or contents in self.options.get(
            "text_content"
        ), f"Could not find the {contents} in the email"
        return self

    def getHtmlContents(self) -> str:
        return self.options.get("html_content")

    def getTextContents(self) -> str:
        return self.options.get("text_content")

    def seeEmailCountEquals(self, count: int) -> "MockMail":
        assert (
            count == self.count
        ), f"Email count of {self.count} does not match expected {count}"
        return self

    def seeEmailDoesNotContain(self, contents: str) -> "MockMail":
        assert contents not in self.options.get(
            "html_content"
        ) and contents not in self.options.get(
            "text_content"
        ), f"Found {contents} in the email but should not be"
        return self

    def seeEmailFrom(self, assertion: str) -> "MockMail":
        assert assertion == self.options.get(
            "from"
        ), f"Assertion of from address {self.options.get('from')} does not match expected {assertion}"
        return self

    def seeEmailReplyTo(self, assertion: str) -> "MockMail":
        assert assertion == self.options.get(
            "reply_to"
        ), f"Assertion of reply-to {self.options.get('reply_to')} does not match expected {assertion}"
        return self

    def seeEmailSubjectContains(self, assertion: str) -> "MockMail":
        assert assertion in self.options.get(
            "subject"
        ), f"Assertion of subject {self.options.get('subject')} does not contain expected {assertion}"
        return self

    def seeEmailSubjectDoesNotContain(self, assertion: str) -> "MockMail":
        assert assertion not in self.options.get(
            "subject"
        ), f"Assertion of subject {self.options.get('subject')} does contain expected {assertion}"
        return self

    def seeEmailSubjectEquals(self, assertion: str) -> "MockMail":
        assert assertion == self.options.get(
            "subject"
        ), f"Assertion of subject address {self.options.get('subject')} does not match expected {assertion}"
        return self

    def seeEmailTo(self, assertion: str) -> "MockMail":
        assert assertion == self.options.get(
            "to"
        ), f"Assertion of to address {self.options.get('to')} does not match expected {assertion}"
        return self

    def seeEmailPriority(self, assertion: int) -> "MockMail":
        assert str(assertion) == self.options.get(
            "priority"
        ), f"Assertion of priority {self.options.get('priority')} does not match expected {assertion}"
        return self

    def seeEmailWasNotSent(self) -> "MockMail":
        assert self.count == 0, "Expected email was not sent but it was sent"
        return self

    def seeEmailWasSent(self) -> "MockMail":
        assert self.count > 0, "Expected email was not sent but it was sent"
        return self

    def seeDriverWas(self, name: str) -> "MockMail":
        assert (
            self.driver == name
        ), f"Expected email driver to be {name} but it was {self.driver}"
        return self
