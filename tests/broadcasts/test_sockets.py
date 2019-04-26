import os

from masonite.drivers import BroadcastAblyDriver, BroadcastPusherDriver
from masonite.managers import BroadcastManager
from masonite.testsuite.TestSuite import TestSuite
import unittest

if os.getenv('ABLY_SECRET'):

    class TestSockets(unittest.TestCase):
            
        def setUp(self):
            self.app = TestSuite().create_container().container
            self.app.bind('BroadcastPusherDriver', BroadcastPusherDriver)
            self.app.bind('BroadcastManager', BroadcastManager)

        def test_broadcast_loads_into_container(self):
            self.app.bind('Broadcast', self.app.make('BroadcastManager').driver('pusher'))

            self.assertIsNotNone(self.app.make('BroadcastManager'))
            self.assertEqual(self.app.make('Broadcast').channel('random', 'from driver'), {'message': 'from driver'})
            self.assertEqual(self.app.make('Broadcast').channel('random', {'message': 'dictionary'}), {'message': 'dictionary'})
            self.assertEqual(self.app.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}), {'message': 'dictionary'})
            self.assertEqual(self.app.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}, 'test-event'), {'message': 'dictionary'})
            self.assertTrue(self.app.make('Broadcast').ssl(True).ssl_message)

        def test_broadcast_loads_into_container_with_ably(self):
            self.app.bind('Broadcast', self.app.make('BroadcastManager').driver('ably'))

            self.assertIsNotNone(self.app.make('BroadcastManager'))
            self.assertEqual(self.app.make('Broadcast').channel('test-channel', 'from driver'), 'from driver')
            self.assertEqual(self.app.make('Broadcast').channel('test-channel', {'message': 'from driver'}), {'message': 'from driver'})
            self.assertEqual(self.app.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}), {'message': 'dictionary'})
            self.assertEqual(self.app.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}, 'test-event'), {'message': 'dictionary'})
            self.assertTrue(self.app.make('Broadcast').ssl(True).ssl_message)
