"""A RedirectionProvider Service Provider."""

from ..drivers import BroadcastAblyDriver, BroadcastPusherDriver
from ..managers import BroadcastManager
from ..provider import ServiceProvider
from .. import Broadcast
from ..helpers import config


class BroadcastProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('BroadcastPusherDriver', BroadcastPusherDriver)
        self.app.bind('BroadcastAblyDriver', BroadcastAblyDriver)
        self.app.bind('BroadcastManager', BroadcastManager(self.app))

    def boot(self):
        self.app.bind('Broadcast', self.app.make('BroadcastManager').driver(config('broadcast.driver')))
        self.app.swap(Broadcast, self.app.make('BroadcastManager').driver(config('broadcast.driver')))
