from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..foundation import Application


class PresenceChannel:
    """Presence Broadcast Channel."""

    def __init__(self, name: str):
        if not name.startswith("presence-"):
            name = "presence-" + name

        self.name = name

    def authorized(self, application: "Application") -> bool:
        """Define is authorized to broadcast event. The base implementation is checking that
        the user is authenticated."""
        return bool(application.make("request").user())
