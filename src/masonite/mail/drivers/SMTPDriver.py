import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from ..Recipient import Recipient
import ssl


class SMTPDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def get_mime_message(self):
        message = MIMEMultipart("alternative")

        message["Subject"] = self.options.get("subject")

        message["From"] = Recipient(self.options.get("from")).header()
        message["To"] = Recipient(self.options.get("to")).header()
        if self.options.get("reply_to"):
            message["Reply-To"] = Recipient(self.options.get("reply_to")).header()

        if self.options.get("cc"):
            message["Cc"] = Recipient(self.options.get("cc")).header()

        if self.options.get("bcc"):
            message["Bcc"] = Recipient(self.options.get("bcc")).header()

        if self.options.get("html_content"):
            message.attach(MIMEText(self.options.get("html_content"), "html"))

        if self.options.get("text_content"):
            message.attach(MIMEText(self.options.get("text_content"), "plain"))

        if self.options.get("priority"):
            message["X-Priority"] = self.options.get("priority")

        if self.options.get("headers"):
            for header, value in self.options.get("headers").items():
                message[header] = value

        for attachment in self.options.get("attachments", []):
            with open(attachment.path, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=attachment.alias)

            part["Content-Disposition"] = f"attachment; filename={attachment.alias}"
            message.attach(part)

        return message

    def make_connection(self):
        options = self.options
        if options.get("ssl"):
            smtp = smtplib.SMTP_SSL("{0}:{1}".format(options["host"], options["port"]))
        else:
            smtp = smtplib.SMTP("{0}:{1}".format(options["host"], int(options["port"])))

        if options.get("tls"):
            context = ssl.create_default_context()
            context.check_hostname = False

            # Check if correct response code for starttls is received from the server
            if smtp.starttls(context=context)[0] != 220:
                raise smtplib.SMTPNotSupportedError(
                    "Server is using untrusted protocol."
                )

        if options.get("username") and options.get("password"):
            smtp.login(options.get("username"), options.get("password"))

        return smtp

    def send(self):
        smtp = self.make_connection()
        smtp.send_message(self.get_mime_message())
