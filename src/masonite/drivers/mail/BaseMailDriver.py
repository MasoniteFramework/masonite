"""Base mail driver module."""

import copy
import re

from masonite.helpers import deprecated

from ...app import App
from ...helpers import config
from ...response import Responsable
from .. import BaseDriver


MAIL_FROM_RE = re.compile(r'(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)')


class BaseMailDriver(BaseDriver, Responsable):
    """Base mail driver class. This class is inherited by all mail drivers."""

    def __init__(self, app: App):
        """Base mail driver constructor.

        Arguments:
            app {masonite.app.App} -- The Masonite container class.
            view {object} -- This is the masonite.view.View class.
        """
        self.config = config('mail')
        self.app = app
        self.to_addresses = []
        self.message_subject = 'Subject'
        self.message_reply_to = None
        self.from_name = self.config.FROM['name']
        self.from_address = self.config.FROM['address']
        self._queue = False
        self.html_content = None
        self.text_content = None
        self._message = None

    def _get_message_for_send_deprecated(self, message_contents):
        """Helper method for backwards compatibility to generate a message from .send()

        Args:
            message_contents: String

        Returns:
            message
        """
        # we used to not override self.message_body, so save it and set it back...
        old_text, old_html = self.text_content, self.html_content
        self.text_content, self.html_content = None, message_contents
        data = self.message()
        self.text_content, self.html_content = old_text, old_html
        return data

    def message(self):
        """Creates a message object for the underlying driver.

        Returns:
            message
        """
        raise NotImplementedError

    @property
    def mail_from_header(self):
        return '"{0}" <{1}>'.format(self.from_name, self.from_address)

    @property
    def mail_to_header(self):
        return ','.join(self.to_addresses)

    def text(self, content):
        """Set the text content of the email.

        Arguments:
            content {string} -- The email text content.

        Returns:
            self
        """
        self.text_content = content
        return self

    def html(self, content):
        """Set the html content of the email.

        Arguments:
            content {string} -- The email html content.

        Returns:
            self
        """
        self.html_content = content
        return self

    @property
    def message_body(self):
        """Returns the body of the message.
        """
        return self.html_content or self.text_content

    @message_body.setter
    @deprecated('Please use `.text()` and `.html()` methods instead.')
    def message_body(self, value):
        self.html_content = value

    def to(self, user_email):
        """Set the user email address who you want to send mail to.

        Arguments:
            user_email {string} -- The user email address.

        Returns:
            self
        """
        if callable(user_email):
            user_email = user_email.email

        if isinstance(user_email, (list, tuple)):
            self.to_addresses = user_email
        else:
            self.to_addresses = [user_email]
        return self

    def queue(self):
        """Whether the email should be queued or not when sending.

        Returns:
            self
        """
        self._queue = True
        return self

    def template(self, template_name, dictionary={}, mimetype='html'):
        """Create an email from a normal Jinja template.

        Arguments:
            template_name {string} -- The name of the template.

        Keyword Arguments:
            dictionary {dict} -- The data to be passed to the template. (default: {{}})
            mimetype {string} -- whether it is html or text content. (default: {html})

        Returns:
            self
        """
        view = copy.copy(self.app.make('ViewClass'))
        content = view.render(template_name, dictionary).rendered_template
        if mimetype == 'html':
            self.html(content)
        else:
            self.text(content)
        return self

    def send_from(self, address, name=None):
        """Set the from address of who the sender should be.

        Arguments:
            address {string} -- A email address used as the From field in an email.
                                "John S" <john@example.com>
                                John S <john@example.com>
                                john@example.com
            name {string} -- A name used as the From field in an email.

        Returns:
            self
        """
        match = MAIL_FROM_RE.match(address)
        if not match:
            raise ValueError('Invalid address specified')

        match_name, match_address = match.groups()
        self.from_address = match_address
        if name is None and match_name:
            self.from_name = match_name

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

    def get_response(self):
        return self.message_body

    def reply_to(self, reply_to):
        """Set the Reply-To of an email.

        Arguments:
            reply_to {string} -- The reply-to of the email

        Returns:
            self
        """
        self.message_reply_to = reply_to
        return self
