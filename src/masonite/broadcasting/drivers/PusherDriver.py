from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from ...foundation import Application
    from pusher import Pusher


class PusherDriver:
    def __init__(self, application: "Application"):
        self.application = application
        self.connection: "Pusher" = None

    def set_options(self, options: dict) -> "PusherDriver":
        self.options = options
        return self

    def get_connection(self) -> "Pusher":
        try:
            import pusher
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'pusher' library. Run 'pip install pusher' to fix this."
            )

        if self.connection:
            return self.connection

        self.connection = pusher.Pusher(
            app_id=str(self.options.get("app_id")),
            key=self.options.get("client"),
            secret=self.options.get("secret"),
            cluster=self.options.get("cluster"),
            host=self.options.get("host"),
            port=self.options.get("port"),
            ssl=self.options.get("ssl"),
        )

        return self.connection

    def channel(self, channels: "str|list", event: "str|Any", value: Any):
        return self.get_connection().trigger(channels, event, value)

    def authorize(self, channel: "str", socket_id: Any) -> dict:
        return self.get_connection().authenticate(channel=channel, socket_id=socket_id)
