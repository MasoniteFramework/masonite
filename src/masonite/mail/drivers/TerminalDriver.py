from ..Recipient import Recipient


class TerminalDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}
        self.content_type = None

    def set_options(self, options):
        self.options = options
        return self

    def send(self):
        print("-------------------------------------")
        print(f"To: {Recipient(self.options.get('to')).header()}")
        print(f"From: {Recipient(self.options.get('from')).header()}")
        print(f"Cc: {Recipient(self.options.get('cc')).header()}")
        print(f"Bcc: {Recipient(self.options.get('bcc')).header()}")
        print(f"Subject: {self.options.get('subject')}")
        if self.options.get("headers"):
            for header, value in self.options.get("headers").items():
                print(f"{header}: {value}")
        print("-------------------------------------")
        print(f"{self.options.get('html_content')}")
        if self.options.get("text_content"):
            print("-------------------------------------")
            print(f"Text Content: {self.options.get('text_content')}")
        if self.options.get("attachments"):
            print("-------------------------------------")
            for index, attachment in enumerate(self.options.get("attachments")):
                index += 1
                print(f"Attachment {index}: {attachment.alias} from {attachment.path}")
