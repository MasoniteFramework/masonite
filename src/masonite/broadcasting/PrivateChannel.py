from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..foundation import Application


class PrivateChannel:
    """Private Broadcast Channel."""

    def __init__(self, name: str):
        if not name.startswith("private-"):
            name = "private-" + name

        self.name = name

    def authorized(self, application: "Application") -> bool:
        """Define is authorized to broadcast event. The base implementation is checking that
        the user is authenticated."""
        return bool(application.make("request").user())
