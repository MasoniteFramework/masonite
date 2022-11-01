from typing import TYPE_CHECKING, Any

from ..routes import Route

if TYPE_CHECKING:
    from ..foundation import Application


class Broadcast:
    def __init__(self, application: "Application", store_config: dict = {}):
        self.application = application
        self.drivers: dict = {}
        self.store_config = store_config
        self.options: dict = {}

    def add_driver(self, name: str, driver: Any):
        self.drivers.update({name: driver})

    def set_configuration(self, config: dict) -> "Broadcast":
        self.store_config = config
        return self

    def get_driver(self, name: str = None) -> Any:
        if name is None:
            return self.drivers[self.store_config.get("default")]
        return self.drivers[name]

    def driver(self, name: str = None) -> Any:
        store_config = self.get_config_options()
        driver = self.get_driver(None)
        return driver.set_options(store_config)

    def get_config_options(self, name: str = None) -> dict:
        if name is None or name == "default":
            return self.store_config.get(self.store_config.get("default"))

        return self.store_config.get(name)

    def channel(
        self,
        channels: "str|list",
        event: "str|Any" = None,
        value: Any = None,
        driver: Any = None,
    ):
        """Broadcast the given event with value on given channels for the specified (or default)
        driver."""
        store_config = self.get_config_options()
        driver = self.get_driver(driver)
        if not isinstance(event, str):
            if event is None:
                event = channels
                channels = event.broadcast_on()

            value = event.broadcast_with()
            if not isinstance(channels, list):
                channels = [channels]

            for channel in channels:
                if not channel.authorized(self.application):
                    continue
                event_class = event.broadcast_as()

                driver.set_options(store_config).channel(
                    channel.name, event_class, value
                )
        else:
            if not isinstance(channels, list):
                channels = [channels]
            for channel in channels:
                driver.set_options(store_config).channel(channel, event, value)

    @classmethod
    def routes(self, auth_route: str = "/broadcasting/authorize") -> list:
        """Get broadcasting authorization routes list used for private and presence channels."""
        from .controllers import BroadcastingController

        return [
            Route.post(auth_route, BroadcastingController.authorize).name(
                "broadcasting.authorize"
            )
        ]
