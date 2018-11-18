"""A RedirectionProvider Service Provider."""

from config import queue
from masonite.drivers import QueueAsyncDriver, QueueAmqpDriver
from masonite.managers import QueueManager
from masonite.provider import ServiceProvider
from masonite import Queue


class QueueProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueAmqpDriver', QueueAmqpDriver)
        self.app.bind('QueueManager', QueueManager)
        self.app.bind('QueueConfig', queue)

    def boot(self, queue: QueueManager):
        self.app.bind('Queue', queue(self.app).driver(self.app.make('QueueConfig').DRIVER))
        self.app.swap(Queue, queue(self.app).driver(self.app.make('QueueConfig').DRIVER))
