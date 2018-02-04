class BaseMailDriver(object):

    def __init__(self, MailConfig):
        self.config = MailConfig
        self.to_address = None
        self.from_address = self.config.FROM
        self.message_subject = 'Subject'

    def to(self, user_email):
        if callable(user_email):
            user_email = user_email.email

        self.to_address = user_email
        return self

    def send_from(self, address):
        self.from_address = address
        return self

    def subject(self, subject):
        self.message_subject = subject
        return self

