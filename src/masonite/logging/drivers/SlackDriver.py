import logging
import requests
from typing import Dict, Any, Optional, Tuple


from .BaseDriver import BaseDriver


class SlackHandler(logging.Handler):
    def __init__(self, url: str) -> None:
        self.url = url
        super(SlackHandler, self).__init__()
        return

    def emit(self, record: logging.LogRecord) -> None:
        """emits message"""
        msg: str = self.format(record)
        requests.post(
            self.url, data=str.encode(msg), headers={"Content-type": "application/json"}
        )
        return


class SlackFormatter(logging.Formatter):
    def __init__(self, name: str) -> None:
        self.name = name
        super(SlackFormatter, self).__init__()
        return

    def format(self, record: logging.LogRecord) -> str:
        import json

        def get_traceback() -> str:
            """returns traceback"""
            from traceback import format_exception

            exc_info: Tuple = record.exc_info
            return "".join(format_exception(*exc_info)) if exc_info else "None"

        def get_color(level: int) -> Optional[str]:
            """returns appropriate color based on logging level"""
            colors: Dict[int, Optional[str]] = {
                0: None,
                10: "#FF00FF",
                20: "good",
                30: "warning",
                40: "danger",
                50: "#660000",
            }
            return colors[level]

        data: Dict[str, Any] = {
            "attachments": [
                {
                    "color": get_color(record.levelno),
                    "title": self.name,
                    "text": record.getMessage(),
                    "fields": [
                        {"title": "Module", "value": record.module, "short": True},
                        {
                            "title": "Level",
                            "value": record.levelname.title(),
                            "short": True,
                        },
                        # {"title": "Function", "value": record.funcName, "short": True},
                        # {"title": "Line Number", "value": record.lineno, "short": True},
                        # {
                        #     "title": "Traceback",
                        #     "value": get_traceback(),
                        #     "short": False,
                        # },
                    ],
                    "ts": int(record.created),
                }
            ]
        }
        return json.dumps(data)


class SlackDriver(BaseDriver):
    """Log message to Slack with Slack API."""

    def __init__(self, application, name, options):
        super().__init__(application, name, options)
        self.logging_handler = SlackHandler(self.options.get("webhook_url"))
        self.logging_handler.setFormatter(SlackFormatter(self.name))
        self.logging_logger = logging.getLogger(self.name)

    def send(self, level, message):
        self.set_logger()
        self.logging_logger.log(
            level, message, extra={"timestamp": self.get_formatted_time()}
        )

    # def send(self, level, message):
    #     # here we don't rely on logging module so we have to build
    #     text = self.get_format()
    #     # level, message, extra={"timestamp": self.get_formatted_time()}
    #     payload = {
    #         "token": self.token,
    #         "channel": self.find_channel(self.channel),
    #         "text": message,
    #         "username": self.username,
    #         "icon_emoji": self.emoji,
    #         "as_user": False,
    #         "reply_broadcast": True,
    #         "unfurl_links": True,
    #         "unfurl_media": True,
    #     }
    #     response = requests.post(self.send_url, payload).json()
    #     if not response["ok"]:
    #         raise Exception("{}. Check Slack API docs.".format(response["error"]))

    # def find_channel(self, name):
    #     """Calls the Slack API to find the channel name.
    #     This is so we do not have to specify the channel ID's. Slack requires channel ID's
    #     to be used.
    #     Arguments:
    #         name {string} -- The channel name to find.
    #     Raises:
    #         SlackChannelNotFound -- Thrown if the channel name is not found.
    #     Returns:
    #         self
    #     """
    #     response = requests.post(
    #         "https://slack.com/api/channels.list", {"token": self.token}
    #     )

    #     for channel in response.json()["channels"]:
    #         if channel["name"] == name.split("#")[1]:
    #             return channel["id"]

    #     raise SlackChannelNotFound("Could not find the {} channel".format(name))
