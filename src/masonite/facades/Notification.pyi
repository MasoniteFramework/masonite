from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..notification import Notification as NotificationObject, AnonymousNotifiable

class Notification:
    """Notification handler facade, which handle sending/queuing notifications anonymously
    or to notifiables through different channels."""

    def add_driver(self, name: str, driver: str): ...
    def get_driver(self, name: str) -> Any: ...
    def set_configuration(self, config: dict) -> "Notification": ...
    def get_config_options(self, driver: str) -> dict: ...
    def send(
        self,
        notifiables: list,
        notification: "NotificationObject",
        drivers: list = [],
        dry: bool = False,
        fail_silently: bool = False,
    ) -> Any:
        """Send the given notification to the given notifiables."""
        ...
    def route(self, driver: str, route: str) -> Any:
        """Specify how to send a notification to an anonymous notifiable."""
        ...
