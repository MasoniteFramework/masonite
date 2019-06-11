import unittest

from masonite.app import App
from masonite.drivers import QueueAmqpDriver, QueueAsyncDriver
from masonite.environment import LoadEnvironment, env
from masonite.exceptions import QueueException
from masonite.managers import QueueManager
from masonite.queues.Queueable import Queueable

from config import queue

LoadEnvironment()


class Job(Queueable):

    def handle(self):
        print('sending from job handled')
        return 'test'


class Random(Queueable):

    def send(self):
        print('sending from random send method')
        return 'test'

    def handle(self):
        print('sending from random handle method')
        return 'test'


class TestQueueDrivers(unittest.TestCase):

    def setUp(self):
        self.app = App()

        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueAmqpDriver', QueueAmqpDriver)
        self.app.bind('QueueConfig', queue)
        self.app.bind('Queueable', Queueable)
        self.app.bind('Container', self.app)
        self.app.bind('QueueManager', QueueManager(self.app))
        self.app.bind('Queue', QueueManager(self.app).driver(self.app.make('QueueConfig').DRIVER))
        self.drivers = ['async']
        self.modes = ['threading', 'multiprocess']

        if env('RUN_AMQP'):
            self.drivers.append('amqp')

    def test_async_driver_pushes_to_queue(self):
        for driver in self.drivers:
            self.assertIsNone(self.app.make('QueueManager').driver(driver).push(Job), None)

    def test_async_driver_can_run_any_callback_method(self):
        for driver in self.drivers:
            self.assertIsNone(self.app.make('QueueManager').driver(driver).push(Random, callback="send"), None)

    def test_async_driver_can_run_any_method(self):
        for driver in self.drivers:
            self.assertIsNone(self.app.make('QueueManager').driver(driver).push(Random().send), None)

    def test_should_return_default_driver(self):
        self.assertIsInstance(self.app.make('Queue'), QueueAsyncDriver)
        self.assertIsInstance(self.app.make('Queue').driver('async'), QueueAsyncDriver)
        self.assertIsInstance(self.app.make('Queue').driver('default'), QueueAsyncDriver)

    def test_async_driver_modes(self):
        for mode in self.modes:
            self.assertIsNone(self.app.make('QueueManager').driver('async').push(Job, mode=mode), None)

    def test_async_driver_finds_mode(self):
        self.assertIsNone(self.app.make('QueueManager').driver('async').push(Job), None)

    def test_handle_unrecognized_mode(self):
        with self.assertRaises(QueueException):
            self.app.make('QueueManager').driver('async').push(Job, mode='blah')

    def test_async_driver_specify_workers(self):
        for mode in self.modes:
            self.assertIsNone(self.app.make('QueueManager').driver('async').push(Job, mode=mode, workers=2), None)

    def test_workers_are_nonnegative(self):
        with self.assertRaises(QueueException):
            for mode in self.modes:
                self.assertIsNone(self.app.make('QueueManager').driver('async').push(Job, mode=mode, workers=-1))
