"""A RedirectionProvider Service Provider."""

from config import broadcast
from masonite.drivers import BroadcastAblyDriver, BroadcastPusherDriver
from masonite.managers import BroadcastManager
from masonite.provider import ServiceProvider
from masonite import Broadcast


class BroadcastProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('BroadcastConfig', broadcast)
        self.app.bind('BroadcastPusherDriver', BroadcastPusherDriver)
        self.app.bind('BroadcastAblyDriver', BroadcastAblyDriver)
        self.app.bind('BroadcastManager', BroadcastManager(self.app))

    def boot(self, broadcast: BroadcastManager):
        self.app.bind('Broadcast', self.app.make('BroadcastManager').driver(self.app.make('BroadcastConfig').DRIVER))
        self.app.swap(Broadcast, self.app.make('BroadcastManager').driver(self.app.make('BroadcastConfig').DRIVER))
