from typing import Any


class CanBroadcast:
    def broadcast_on(self) -> "str|list":
        """Channel or list of channels to broadcast on."""
        return None

    def broadcast_with(self) -> Any:
        """Data to broadcast."""
        return vars(self)

    def broadcast_as(self) -> str:
        """Name of the event to broadcast as."""
        return self.__class__.__name__
