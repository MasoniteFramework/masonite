from masonite.drivers.BaseDriver import BaseDriver
from masonite.view import view


class BaseMailDriver(BaseDriver):
    """Base mail driver class. This class is inherited by all mail drivers.
    """

    def __init__(self, MailConfig, View):
        self.config = MailConfig
        self.to_address = None
        self.from_address = self.config.FROM
        self.message_subject = 'Subject'
        self.message_body = None
        self.view = View

    def to(self, user_email):
        if callable(user_email):
            user_email = user_email.email

        self.to_address = user_email
        return self

    def template(self, template_name, dictionary={}):
        self.message_body = self.view.render(template_name, dictionary).rendered_template
        return self

    def send_from(self, address):
        self.from_address = address
        return self

    def subject(self, subject):
        self.message_subject = subject
        return self
