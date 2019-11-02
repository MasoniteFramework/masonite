import os

from src.masonite.drivers import BroadcastPusherDriver
from src.masonite.managers import BroadcastManager
from src.masonite.testing import TestCase

if os.getenv('ABLY_SECRET'):

    class TestSockets(TestCase):

        def setUp(self):
            super().setUp()
            self.container.bind('BroadcastPusherDriver', BroadcastPusherDriver)
            self.container.bind('BroadcastManager', BroadcastManager)

        def test_broadcast_loads_into_container(self):
            self.container.bind('Broadcast', self.container.make('BroadcastManager').driver('pusher'))

            self.assertIsNotNone(self.container.make('BroadcastManager'))
            self.assertEqual(self.container.make('Broadcast').channel('random', 'from driver'), {'message': 'from driver'})
            self.assertEqual(self.container.make('Broadcast').channel('random', {'message': 'dictionary'}), {'message': 'dictionary'})
            self.assertEqual(self.container.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}), {'message': 'dictionary'})
            self.assertEqual(self.container.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}, 'test-event'), {'message': 'dictionary'})
            self.assertTrue(self.container.make('Broadcast').ssl(True).ssl_message)

        def test_broadcast_loads_into_container_with_ably(self):
            self.container.bind('Broadcast', self.container.make('BroadcastManager').driver('ably'))

            self.assertIsNotNone(self.container.make('BroadcastManager'))
            self.assertEqual(self.container.make('Broadcast').channel('test-channel', 'from driver'), 'from driver')
            self.assertEqual(self.container.make('Broadcast').channel('test-channel', {'message': 'from driver'}), {'message': 'from driver'})
            self.assertEqual(self.container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}), {'message': 'dictionary'})
            self.assertEqual(self.container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}, 'test-event'), {'message': 'dictionary'})
            self.assertTrue(self.container.make('Broadcast').ssl(True).ssl_message)
