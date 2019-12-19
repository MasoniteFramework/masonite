"""Base mail driver module."""

from masonite.drivers import BaseDriver
from masonite.app import App
import copy


class BaseMailDriver(BaseDriver):
    """Base mail driver class. This class is inherited by all mail drivers."""

    def __init__(self, app: App):
        """Base mail driver constructor.

        Arguments:
            app {masonite.app.App} -- The Masonite container class.
            view {object} -- This is the masonite.view.View class.
        """
        self.config = app.make('MailConfig')
        self.app = app
        self.to_address = None
        self.from_address = self.config.FROM
        self.message_subject = 'Subject'
        self.message_reply_to = None
        self.message_body = None
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
        """Whether the email should be queued or not when sending.

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
        view = copy.copy(self.app.make('ViewClass'))
        self.message_body = view.render(template_name, dictionary).rendered_template
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

    def mailable(self, mailable):
        """Set the from address of who the sender should be.

        Arguments:
            address {string} -- A name used as the From field in an email.

        Returns:
            self
        """
        mailable = self.app.resolve(mailable.build)
        (self
            .to(mailable._to)
            .send_from(mailable._from)
            .subject(mailable._subject)
            .template(mailable.template, mailable.variables)
            .reply_to(mailable._reply_to))
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

    def reply_to(self, reply_to):
        """Set the Reply-To of an email.

        Arguments:
            reply_to {string} -- The reply-to of the email

        Returns:
            self
        """
        self.message_reply_to = reply_to
        return self
