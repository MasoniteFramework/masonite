from masonite.app import App
from masonite.drivers import QueueAsyncDriver, QueueAmqpDriver
from masonite.managers import QueueManager
from config import queue

from masonite.queues.Queueable import Queueable
import os
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

        assert self.app.make('QueueManager') == 'async'

        assert self.app.make('QueueManager').driver('async') == 'async'

        assert self.app.make('QueueManager').driver('default') == 'async'
