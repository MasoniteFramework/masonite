import os

from masonite.drivers.BroadcastAblyDriver import BroadcastAblyDriver
from masonite.drivers.BroadcastPusherDriver import BroadcastPusherDriver
from masonite.managers.BroadcastManager import BroadcastManager
from masonite.testsuite.TestSuite import TestSuite

from config import broadcast

if os.getenv('ABLY_SECRET'):

    class TestSockets:

        def setup_method(self):
            self.app = TestSuite().create_container().container
            self.app.bind('BroadcastConfig', broadcast)
            self.app.bind('BroadcastPusherDriver', BroadcastPusherDriver)
            self.app.bind('BroadcastManager', BroadcastManager().load_container(self.app))

        def test_broadcast_loads_into_container(self):

            self.app.bind('Broadcast', self.app.make('BroadcastManager').driver('pusher'))

            assert self.app.make('BroadcastManager')
            assert self.app.make('Broadcast').channel('random', 'from driver') == {'message': 'from driver'}
            assert self.app.make('Broadcast').channel('random', {'message': 'dictionary'}) == {'message': 'dictionary'}
            assert self.app.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}) == {'message': 'dictionary'}
            assert self.app.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}, 'test-event') == {'message': 'dictionary'}
            assert self.app.make('Broadcast').ssl(True).ssl_message is True

        def test_broadcast_loads_into_container_with_ably(self):
            self.app.bind('Broadcast', self.app.make('BroadcastManager').driver('ably'))

            assert self.app.make('BroadcastManager')
            assert self.app.make('Broadcast').channel('test-channel', 'from driver') == 'from driver'
            assert self.app.make('Broadcast').channel('test-channel', {'message': 'from driver'}) == {'message': 'from driver'}
            assert self.app.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}) == {'message': 'dictionary'}
            assert self.app.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}, 'test-event') == {'message': 'dictionary'}
            assert self.app.make('Broadcast').ssl(True).ssl_message is True
