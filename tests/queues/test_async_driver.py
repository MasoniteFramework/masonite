from masonite.app import App
from masonite.drivers.QueueAsyncDriver import QueueAsyncDriver
from masonite.managers.QueueManager import QueueManager
from config import queue

from masonite.queues.Queueable import Queueable


class Job(Queueable):

    def handle(self):
        return 'test'


class TestAsyncDriver:

    def setup_method(self):
        self.app = App()

        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueConfig', queue)
        self.app.bind('Queueable', Queueable)
        self.app.bind('Container', self.app)
        self.app.bind('QueueManager', QueueManager(self.app))

    def test_async_driver_pushes_to_queue(self):
        assert self.app.make('QueueManager').driver('async').push(Job) is None
