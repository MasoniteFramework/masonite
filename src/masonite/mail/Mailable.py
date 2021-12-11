from .MessageAttachment import MessageAttachment


class Mailable:
    def __init__(self):
        self._to = ""
        self._cc = ""
        self._bcc = ""
        self._from = ""
        self._reply_to = ""
        self._subject = ""
        self._priority = None
        self._driver = None
        self.text_content = ""
        self.html_content = ""
        self.attachments = []
        self.headers = {}

    def to(self, to):
        self._to = to
        return self

    def cc(self, cc):
        self._cc = cc
        return self

    def bcc(self, bcc):
        self._bcc = bcc
        return self

    def header(self, key, value):
        self.headers.update({key: value})
        return self

    def set_application(self, application):
        self.application = application
        return self

    def from_(self, _from):
        self._from = _from
        return self

    def attach(self, name, path):
        self.attachments.append(MessageAttachment(name, path))
        return self

    def reply_to(self, reply_to):
        self._reply_to = reply_to
        return self

    def subject(self, subject):
        self._subject = subject
        return self

    def text(self, content):
        self.text_content = content
        return self

    def html(self, content):
        self.html_content = content
        return self

    def view(self, view, data={}):
        return self.html(
            self.application.make("view").render(view, data).rendered_template
        )

    def priority(self, priority):
        self._priority = str(priority)
        return self

    def high_priority(self):
        self.priority(1)
        return self

    def low_priority(self):
        self.priority(5)
        return self

    def driver(self, driver):
        self._driver = driver
        return self

    def get_response(self):
        self.build()
        if self.get_options().get("html_content"):
            return self.get_options().get("html_content")
        if self.get_options().get("text_content"):
            return self.get_options().get("text_content")

    def get_options(self):
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

    def build(self, *args, **kwargs):
        return self
