from typing import TYPE_CHECKING

from .MessageAttachment import MessageAttachment

if TYPE_CHECKING:
    from ..foundation import Application


class Mailable:
    """Mailable class allowing to build an e-mail easily."""

    def __init__(self):
        self._to = ""
        self._cc = ""
        self._bcc = ""
        self._from = ""
        self._reply_to = ""
        self._subject: str = ""
        self._priority = None
        self._driver: str = None
        self.text_content: str = ""
        self.html_content: str = ""
        self.attachments: list = []
        self.headers: dict = {}

    def to(self, to: str) -> "Mailable":
        """Specifies the recipient to send the email to. You may also specify the recipient like
        with 'Joseph <user@example.com>'."""
        self._to = to
        return self

    def cc(self, cc: list) -> "Mailable":
        """Specifies a list of addresses that should be "carbon copied" onto this email."""
        self._cc = cc
        return self

    def bcc(self, bcc: list) -> "Mailable":
        """Specifies a list of addresses that should be "blind carbon copied" onto this email."""
        self._bcc = bcc
        return self

    def header(self, key: str, value) -> "Mailable":
        """Add a HTTP header when sending the e-mail."""
        self.headers.update({key: value})
        return self

    def set_application(self, application: "Application") -> "Mailable":
        self.application = application
        return self

    def from_(self, _from: str) -> "Mailable":
        """Specifies the address that the email should appear it is from. If no from address is
        specified, the default 'mail.mail_from' configuration option will be used."""
        self._from = _from
        return self

    def attach(self, name: str, path: str) -> "Mailable":
        """Attach a file to the email with the given name."""
        self.attachments.append(MessageAttachment(name, path))
        return self

    def reply_to(self, reply_to: str) -> "Mailable":
        """Specifies the address that will be set if a user clicks reply to this email"""
        self._reply_to = reply_to
        return self

    def subject(self, subject: str) -> "Mailable":
        """Specifies the subject of the email."""
        self._subject = subject
        return self

    def text(self, content: str) -> "Mailable":
        """Specifies the plain text version of the email."""
        self.text_content = content
        return self

    def html(self, content: str) -> "Mailable":
        """Specifies the HTML version of the email."""
        self.html_content = content
        return self

    def view(self, view: str, data: dict = {}) -> "Mailable":
        """Specifies a Masonite view file with context data to render the HTML version of the
        email."""
        return self.html(
            self.application.make("view").render(view, data).rendered_template
        )

    def priority(self, priority: int) -> "Mailable":
        """Set the priority of the email (between 1 and 5)."""
        self._priority = str(priority)
        return self

    def high_priority(self) -> "Mailable":
        """Set the priority of the email to the highest (1)."""
        self.priority(1)
        return self

    def low_priority(self) -> "Mailable":
        """Set the priority of the email to the lowest (5)."""
        self.priority(5)
        return self

    def driver(self, driver: str) -> "Mailable":
        """Override the driver to use when sending this mailable."""
        self._driver = driver
        return self

    def get_response(self) -> str:
        """Get mailable response as HTML is html_content has been defined else get response as
        plain text is text_content has been defined."""
        self.build()
        if self.get_options().get("html_content"):
            return self.get_options().get("html_content")
        if self.get_options().get("text_content"):
            return self.get_options().get("text_content")

    def get_options(self) -> dict:
        """Serialize mailable as a dictionary."""
        return {
            "to": self._to,
            "cc": self._cc,
            "bcc": self._bcc,
            "from": self._from,
            "subject": self._subject,
            "text_content": self.text_content,
            "html_content": self.html_content,
            "reply_to": self._reply_to,
            "attachments": self.attachments,
            "priority": self._priority,
            "driver": self._driver,
            "headers": self.headers,
        }

    def build(self, *args, **kwargs) -> "Mailable":
        return self
