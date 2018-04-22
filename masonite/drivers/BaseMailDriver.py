from masonite.view import view
from masonite.drivers.BaseDriver import BaseDriver


class BaseMailDriver(BaseDriver):
    """
    Class base for mail drivers
    """

    def __init__(self, MailConfig):
        self.config = MailConfig
        self.to_address = None
        self.from_address = self.config.FROM
        self.message_subject = 'Subject'
        self.message_body = None

    def to(self, user_email):
        if callable(user_email):
            user_email = user_email.email

        self.to_address = user_email
        return self

    def template(self, template_name, dictionary={}):
        self.message_body = view(template_name, dictionary)
        return self

    def send_from(self, address):
        self.from_address = address
        return self

    def subject(self, subject):
        self.message_subject = subject
        return self
