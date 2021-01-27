import unittest

from src.masonite.app import App
from src.masonite.drivers import QueueAmqpDriver, QueueAsyncDriver, QueueDatabaseDriver
from src.masonite.environment import LoadEnvironment, env
from src.masonite.exceptions import QueueException
from src.masonite.managers import QueueManager
from src.masonite.queues.Queueable import Queueable
from src.masonite.helpers import config

LoadEnvironment()


class Job(Queueable):

    def handle(self):
        print('sending from job handled')
        return 'test'


class FailJob(Queueable):

    def handle(self):
        raise Exception('Failed Job')


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
        self.app.bind('QueueDatabaseDriver', QueueDatabaseDriver)
        self.app.bind('Queueable', Queueable)
        self.app.bind('Container', self.app)
        self.app.bind('QueueManager', QueueManager(self.app))
        self.app.bind('Queue', QueueManager(self.app).driver(config('queue.driver')))
        self.drivers = ['async']
        self.modes = ['threading', 'multiprocess']

        if env('RUN_AMQP'):
            self.drivers.append('amqp')
        if env('RUN_QUEUE_DATABASE'):
            self.drivers.append('database')

    def test_async_driver_pushes_to_queue(self):
        for driver in self.drivers + ['database']:
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

    def test_driver_can_wait(self):
        for driver in self.drivers:
            self.assertIsNone(self.app.make('QueueManager').driver(driver).push(Job, wait='10 seconds'), None)

    def test_driver_can_fail(self):
        for driver in self.drivers:
            self.assertIsNone(self.app.make('QueueManager').driver(driver).push(FailJob), None)

    def test_workers_are_nonnegative(self):
        with self.assertRaises(QueueException):
            for mode in self.modes:
                self.assertIsNone(self.app.make('QueueManager').driver('async').push(Job, mode=mode, workers=-1))
