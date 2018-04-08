''' A RedirectionProvider Service Provider '''
from masonite.provider import ServiceProvider
from masonite.managers.BroadcastManager import BroadcastManager
from masonite.drivers.BroadcastPusherDriver import BroadcastPusherDriver
from masonite.drivers.BroadcastAblyDriver import BroadcastAblyDriver
from config import broadcast


class BroadcastProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('BroadcastConfig', broadcast)
        self.app.bind('BroadcastPusherDriver', BroadcastPusherDriver)
        self.app.bind('BroadcastAblyDriver', BroadcastAblyDriver)
        self.app.bind('BroadcastManager', BroadcastManager(self.app))

    def boot(self, BroadcastConfig, BroadcastManager):
        self.app.bind('Broadcast', self.app.make('BroadcastManager').driver(BroadcastConfig.DRIVER))
