from masonite.app import App
from masonite.drivers.QueueAsyncDriver import QueueAsyncDriver
from masonite.managers.QueueManager import QueueManager
from config import queue

from masonite.queues.Queueable import Queueable

class Job(Queueable):

    def handle(self):
        return 'test'

def test_async_driver_pushes_to_queue():
    container = App()

    container.bind('QueueAsyncDriver', QueueAsyncDriver)
    container.bind('QueueConfig', queue)
    container.bind('Queueable', Queueable)
    container.bind('Container', container)
    container.bind('QueueManager', QueueManager(container))

    assert container.make('QueueManager').driver('async').push(Job) is None