"""Base mail driver module."""

from masonite.drivers.BaseDriver import BaseDriver
from masonite.view import View
from masonite.app import App


class BaseMailDriver(BaseDriver):
    """Base mail driver class. This class is inherited by all mail drivers."""

    def __init__(self, app: App, view: View):
        """Base mail driver constructor.

        Arguments:
            MailConfig {module} -- This is the config.mail module.
            View {object} -- This is the masonite.view.View class.
        """
        self.config = app.make('MailConfig')
        self.to_address = None
        self.from_address = self.config.FROM
        self.message_subject = 'Subject'
        self.message_body = None
        self.view = view
        self._queue = False

    def to(self, user_email):
        """Set the user email address who you want to send mail to.

        Arguments:
            user_email {string} -- The user email address.

        Returns:
            self
        """
        if callable(user_email):
            user_email = user_email.email

        self.to_address = user_email
        return self

    def queue(self):
        """Set the user email address who you want to send mail to.

        Arguments:
            user_email {string} -- The user email address.

        Returns:
            self
        """
        self._queue = True
        return self

    def template(self, template_name, dictionary={}):
        """Create an email from a normal Jinja template.

        Arguments:
            template_name {string} -- The name of the template.

        Keyword Arguments:
            dictionary {dict} -- The data to be passed to the template. (default: {{}})

        Returns:
            self
        """
        self.message_body = self.view.render(template_name, dictionary).rendered_template
        return self

    def send_from(self, address):
        """Set the from address of who the sender should be.

        Arguments:
            address {string} -- A name used as the From field in an email.

        Returns:
            self
        """
        self.from_address = address
        return self

    def subject(self, subject):
        """Set the subject of an email.

        Arguments:
            subject {string} -- The subject of the email

        Returns:
            self
        """
        self.message_subject = subject
        return self
