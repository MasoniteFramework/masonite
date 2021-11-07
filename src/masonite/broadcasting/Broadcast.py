from ..routes import Route


class Broadcast:
    def __init__(self, application, store_config=None):
        self.application = application
        self.drivers = {}
        self.store_config = store_config or {}
        self.options = {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.store_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.store_config.get("default")]
        return self.drivers[name]

    def driver(self, name=None):
        store_config = self.get_config_options()
        driver = self.get_driver(None)
        return driver.set_options(store_config)

    def get_store_config(self, name=None):
        if name is None or name == "default":
            return self.store_config.get(self.store_config.get("default"))

        return self.store_config.get(name)

    def get_config_options(self, name=None):
        if name is None or name == "default":
            return self.store_config.get(self.store_config.get("default"))

        return self.store_config.get(name)

    def channel(self, channels, event=None, value=None, driver=None):
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
    def routes(self, auth_route="/broadcasting/authorize"):
        from .controllers import BroadcastingController

        return [
            Route.post(auth_route, BroadcastingController.authorize).name(
                "broadcasting.authorize"
            )
        ]
