from masonite.app import App
from masonite.drivers import QueueAsyncDriver, QueueAmqpDriver
from masonite.managers import QueueManager
from config import queue
from masonite.exceptions import QueueException
from masonite.queues.Queueable import Queueable
import os
import pytest
from masonite.environment import LoadEnvironment, env

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


class TestAsyncDriver:

    def setup_method(self):
        self.app = App()

        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueAmqpDriver', QueueAmqpDriver)
        self.app.bind('QueueConfig', queue)
        self.app.bind('Queueable', Queueable)
        self.app.bind('Container', self.app)
        self.app.bind('QueueManager', QueueManager(self.app))
        self.app.bind('Queue', QueueManager(self.app).driver(self.app.make('QueueConfig').DRIVER))
        self.drivers = ['async']
       
        if env('RUN_AMQP'):
            self.drivers.append('amqp')

    def test_async_driver_pushes_to_queue(self):
        for driver in self.drivers:
            assert self.app.make('QueueManager').driver(driver).push(Job) is None

    def test_async_driver_can_run_any_callback_method(self):
        for driver in self.drivers:
            assert self.app.make('QueueManager').driver(driver).push(Random, callback="send") is None

    def test_async_driver_can_run_any_method(self):
        for driver in self.drivers:
            assert self.app.make('QueueManager').driver(driver).push(Random().send) is None

    def test_should_return_default_driver(self):
        assert isinstance(self.app.make('Queue'), QueueAsyncDriver)
        assert isinstance(self.app.make('Queue').driver('async'), QueueAsyncDriver)
        assert isinstance(self.app.make('Queue').driver('default'), QueueAsyncDriver)

    def test_async_driver_with_threading(self):
        assert self.app.make('QueueManager').driver('async').push(Job, mode='threading') is None

    def test_async_driver_with_multiprocess(self):
        assert self.app.make('QueueManager').driver('async').push(Job, mode='multiprocess') is None

    def test_handle_unrecognized_mode(self):
        with pytest.raises(QueueException, message="Should raise QueueException error"):
            self.app.make('QueueManager').driver('async').push(Job, mode='blah')

    def test_async_driver_specify_workers(self):
        assert self.app.make('QueueManager').driver('async').push(Job, mode='threading', workers=2) is None
        assert self.app.make('QueueManager').driver('async').push(Job, mode='multiprocess', workers=2) is None
