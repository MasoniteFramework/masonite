import requests
from ..Recipient import Recipient


class MailgunDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}
        self.content_type = None

    def set_options(self, options):
        self.options = options
        return self

    def get_mime_message(self):
        data = {
            "from": self.options.get("from"),
            "to": Recipient(self.options.get("to")).header(),
            "subject": self.options.get("subject"),
            "h:Reply-To": self.options.get("reply_to"),
            "html": self.options.get("html_content"),
            "text": self.options.get("text_content"),
        }

        if self.options.get("cc"):
            data.update({"cc", self.options.get("cc")})
        if self.options.get("bcc"):
            data.update({"bcc", self.options.get("bcc")})
        if self.options.get("priority"):
            data.update({"h:X-Priority", self.options.get("priority")})
        if self.options.get("headers"):
            for header, value in self.options.get("headers").items():
                data.update({f"h:{header}", value})

        return data

    def get_attachments(self):
        files = []
        for attachment in self.options.get("attachments", []):
            files.append(("attachment", open(attachment.path, "rb")))

        return files

    def send(self):
        domain = self.options["domain"]
        secret = self.options["secret"]
        attachments = self.get_attachments()

        return requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", secret),
            data=self.get_mime_message(),
            files=attachments,
        )
