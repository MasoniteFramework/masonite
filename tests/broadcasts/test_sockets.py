import os
import unittest
from src.masonite.drivers import BroadcastPusherDriver
from src.masonite.managers import BroadcastManager
from src.masonite.testing import TestCase


class TestSockets(TestCase):

    def setUp(self):
        super().setUp()
        self.container.bind('BroadcastPusherDriver', BroadcastPusherDriver)
        self.container.bind('BroadcastManager', BroadcastManager)
        # skip tests depending on drivers keys presence
        self.run_pusher_tests = bool(os.getenv('PUSHER_SECRET'))
        self.run_ably_tests = bool(os.getenv('ABLY_SECRET'))
        self.run_pubnub_tests = bool(os.getenv('PUBNUB_SECRET'))

    def test_broadcast_loads_into_container(self):
        if not self.run_pusher_tests:
            self.skipTest("require Pusher keys")
        self.container.bind('Broadcast', self.container.make('BroadcastManager').driver('pusher'))

        self.assertIsNotNone(self.container.make('BroadcastManager'))
        self.assertEqual(self.container.make('Broadcast').channel('random', 'from driver'), {'message': 'from driver'})
        self.assertEqual(self.container.make('Broadcast').channel('random', {'message': 'dictionary'}), {'message': 'dictionary'})
        self.assertEqual(self.container.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}), {'message': 'dictionary'})
        self.assertEqual(self.container.make('Broadcast').channel(['channel1', 'channel2'], {'message': 'dictionary'}, 'test-event'), {'message': 'dictionary'})
        self.assertTrue(self.container.make('Broadcast').ssl(True).ssl_message)

    def test_broadcast_loads_into_container_with_ably(self):
        if not self.run_ably_tests:
            self.skipTest("require Ably keys")
        self.container.bind('Broadcast', self.container.make('BroadcastManager').driver('ably'))

        self.assertIsNotNone(self.container.make('BroadcastManager'))
        self.assertEqual(self.container.make('Broadcast').channel('test-channel', 'from driver'), {'message': 'from driver'})
        self.assertEqual(self.container.make('Broadcast').channel('test-channel', {'message': 'from driver'}), {'message': 'from driver'})
        self.assertEqual(self.container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}), {'message': 'dictionary'})
        self.assertEqual(self.container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}, 'test-event'), {'message': 'dictionary'})
        self.assertTrue(self.container.make('Broadcast').ssl(True).ssl_message)

    def test_broadcast_loads_into_container_with_pubnub(self):
        if not self.run_pubnub_tests:
            self.skipTest("require PubNub keys")
        self.container.bind('Broadcast', self.container.make('BroadcastManager').driver('pubnub'))

        self.assertIsNotNone(self.container.make('BroadcastManager'))
        self.assertEqual(self.container.make('Broadcast').channel('test-channel', 'from driver'), {'message': 'from driver'})
        self.assertEqual(self.container.make('Broadcast').channel('test-channel', {'message': 'from driver'}), {'message': 'from driver'})
        self.assertEqual(self.container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}), {'message': 'dictionary'})
        self.assertEqual(self.container.make('Broadcast').channel(['channel-1', 'channel-2'], {'message': 'dictionary'}, 'test-event'), {'message': 'dictionary'})
        self.assertTrue(self.container.make('Broadcast').ssl(True).ssl_message)
