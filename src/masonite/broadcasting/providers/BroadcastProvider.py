from ...providers import Provider
from ..Broadcast import Broadcast
from ..drivers import PusherDriver
from ...configuration import config


class BroadcastProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        broadcast = Broadcast(self.application).set_configuration(
            config("broadcast.broadcasts")
        )
        broadcast.add_driver("pusher", PusherDriver(self.application))

        self.application.bind("broadcast", broadcast)

    def boot(self):
        pass
