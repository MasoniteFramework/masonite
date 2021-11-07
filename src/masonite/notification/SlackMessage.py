"""Class modelling a Slack message."""
import json


class SlackMessage:
    WEBHOOK_MODE = 1
    API_MODE = 2

    def __init__(self):
        self._text = ""
        self._username = "masonite-bot"
        self._icon_emoji = ""
        self._icon_url = ""
        self._text = ""
        self._mrkdwn = True
        self._as_current_user = False
        self._reply_broadcast = False
        # Indicates if channel names and usernames should be linked.
        self._link_names = False
        # Indicates if you want a preview of links inlined in the message.
        self._unfurl_links = False
        # Indicates if you want a preview of links to media inlined in the message.
        self._unfurl_media = False
        self._blocks = []

        self._token = ""
        self._webhook = ""
        self._mode = None

    def from_(self, username, icon=None, url=None):
        """Set a custom username and optional emoji icon for the Slack message."""
        self._username = username
        if icon:
            self._icon_emoji = icon
        elif url:
            self._icon_url = url
        return self

    def to(self, to):
        """Specifies the channel to send the message to. It can be a list or single
        element. It can be either a channel ID or a channel name (with #), if it's
        a channel name the channel ID will be resolved later.
        """
        self._to = to
        return self

    def text(self, text):
        """Specifies the text to be sent in the message.

        Arguments:
            text {string} -- The text to show in the message.

        Returns:
            self
        """
        self._text = text
        return self

    def link_names(self):
        """Find and link channel names and usernames in message."""
        self._link_names = True
        return self

    def unfurl_links(self):
        """Whether the message should unfurl any links.

        Unfurling is when it shows a bigger part of the message after the text is sent
        like when pasting a link and it showing the header images.

        Returns:
            self
        """
        self._unfurl_links = True
        self._unfurl_media = True
        return self

    def without_markdown(self):
        """Specifies whether the message should explicitly not honor markdown text.

        Returns:
            self
        """
        self._mrkdwn = False
        return self

    def can_reply(self):
        """Whether the message should be ably to be replied back to.

        Returns:
            self
        """
        self._reply_broadcast = True
        return self

    def build(self, *args, **kwargs):
        return self

    def get_options(self):
        options = {
            "text": self._text,
            # optional
            "link_names": self._link_names,
            "unfurl_links": self._unfurl_links,
            "unfurl_media": self._unfurl_media,
            "username": self._username,
            "as_user": self._as_current_user,
            "icon_emoji": self._icon_emoji,
            "icon_url": self._icon_url,
            "mrkdwn": self._mrkdwn,
            "reply_broadcast": self._reply_broadcast,
            "blocks": json.dumps([block._resolve() for block in self._blocks]),
        }
        if self._mode == self.API_MODE:
            options.update({"channel": self._to, "token": self._token})
        return options

    def token(self, token):
        """[API_MODE only] Specifies the token to use for Slack authentication.

        Arguments:
            token {string} -- The Slack authentication token.

        Returns:
            self
        """
        self._token = token
        return self

    def as_current_user(self):
        """[API_MODE only] Send message as the currently authenticated user.

        Returns:
            self
        """
        self._as_current_user = True
        return self

    def webhook(self, webhook):
        """[WEBHOOK_MODE only] Specifies the webhook to use to send the message and authenticate
        to Slack.

        Arguments:
            webhook {string} -- Slack configured webhook url.

        Returns:
            self
        """
        self._webhook = webhook
        return self

    def block(self, block_instance):
        try:
            from slackblocks.blocks import Block
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'slackblocks' library. Run 'pip install slackblocks' to fix this."
            )

        if not isinstance(block_instance, Block):
            raise Exception("Blocks should be imported from 'slackblocks' package.")
        self._blocks.append(block_instance)
        return self

    def mode(self, mode):
        self._mode = mode
        return self
