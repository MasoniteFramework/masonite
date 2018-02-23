from masonite.testsuite.TestSuite import TestSuite
from masonite.managers.BroadcastManager import BroadcastManager
from masonite.drivers.BroadcastPusherDriver import BroadcastPusherDriver
from masonite.drivers.BroadcastAblyDriver import BroadcastAblyDriver
from config import broadcast

import os

if os.getenv('ABLY_SECRET'):
    def test_broadcast_loads_into_container():
        container = TestSuite().create_container().container

        container.bind('BroadcastConfig', broadcast)
        container.bind('BroadcastPusherDriver', BroadcastPusherDriver)
        container.bind('BroadcastManager', BroadcastManager().load_container(container))
        container.bind('Broadcast', container.make('BroadcastManager').driver('pusher'))

        assert container.make('BroadcastManager')
        assert container.make('Broadcast').channel('random', 'from driver') == {'message': 'from driver'}
        assert container.make('Broadcast').channel('random', {'message': 'dictionary'}) == {'message': 'dictionary'}
        assert container.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}) == {'message': 'dictionary'}
        assert container.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}, 'test-event') == {'message': 'dictionary'}

    def test_broadcast_loads_into_container_with_ably():
        container = TestSuite().create_container().container

        container.bind('BroadcastConfig', broadcast)
        container.bind('BroadcastAblyDriver', BroadcastAblyDriver)
        container.bind('BroadcastManager', BroadcastManager().load_container(container))
        container.bind('Broadcast', container.make('BroadcastManager').driver('ably'))

        assert container.make('BroadcastManager')
        assert container.make('Broadcast').channel('test-channel', 'from driver') == 'from driver'
        assert container.make('Broadcast').channel('test-channel', {'message': 'from driver'}) == {'message': 'from driver'}
        assert container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}) == {'message': 'dictionary'}
        assert container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}, 'test-event') == {'message': 'dictionary'}
