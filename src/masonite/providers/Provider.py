from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..foundation import Application


class Provider:
    def __init__(self, application: "Application") -> None:
        self.application = application

    def register(self) -> None:
        """Code to execute once at application start when provider is registered into the app
        container."""
        pass

    def boot(self) -> None:
        """Code to execute when provider are booted at each request."""
        pass
