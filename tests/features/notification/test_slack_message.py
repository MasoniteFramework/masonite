from tests import TestCase
from src.masonite.notification import SlackMessage


class WelcomeToSlack(SlackMessage):
    def build(self):
        return (
            self.to("#general")
            .from_("sam")
            .text("Hello from Masonite!")
            .link_names()
            .unfurl_links()
            .without_markdown()
            .can_reply()
            .mode(2)  # API MODE
        )


class TestSlackMessage(TestCase):
    def test_build_message(self):
        slack_message = WelcomeToSlack().build().get_options()
        self.assertEqual(slack_message.get("channel"), "#general")
        self.assertEqual(slack_message.get("username"), "sam")
        self.assertEqual(slack_message.get("text"), "Hello from Masonite!")
        self.assertEqual(slack_message.get("link_names"), True)
        self.assertEqual(slack_message.get("unfurl_links"), True)
        self.assertEqual(slack_message.get("unfurl_media"), True)
        self.assertEqual(slack_message.get("mrkdwn"), False)
        self.assertEqual(slack_message.get("reply_broadcast"), True)
        self.assertEqual(slack_message.get("as_user"), False)
        self.assertEqual(slack_message.get("blocks"), "[]")

    def test_from_options(self):
        slack_message = SlackMessage().from_("sam", icon=":ghost").build().get_options()
        self.assertEqual(slack_message.get("username"), "sam")
        self.assertEqual(slack_message.get("icon_emoji"), ":ghost")
        self.assertEqual(slack_message.get("icon_url"), "")
        slack_message = SlackMessage().from_("sam", url="#").build().get_options()
        self.assertEqual(slack_message.get("username"), "sam")
        self.assertEqual(slack_message.get("icon_url"), "#")
        self.assertEqual(slack_message.get("icon_emoji"), "")

    def test_build_with_blocks(self):
        from slackblocks import DividerBlock, HeaderBlock

        slack_message = (
            SlackMessage()
            .from_("Sam")
            .text("Hello")
            .block(HeaderBlock("Header title", block_id="1"))
            .block(DividerBlock(block_id="2"))
            .build()
            .get_options()
        )
        self.assertEqual(
            slack_message.get("blocks"),
            '[{"type": "header", "block_id": "1", "text": {"type": "plain_text", "text": "Header title"}}, {"type": "divider", "block_id": "2"}]',
        )

    def test_api_mode_options(self):
        slack_message = SlackMessage().as_current_user().token("123456")
        self.assertEqual(slack_message._token, "123456")
        slack_message_options = slack_message.build().get_options()
        self.assertEqual(slack_message_options.get("as_user"), True)
