from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..foundation import Application


class Channel:
    """Public Broadcast Channel."""

    def __init__(self, name: str):
        self.name = name

    def authorized(self, application: "Application") -> bool:
        """Define is authorized to broadcast event."""
        return True
