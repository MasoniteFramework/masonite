"""A RedirectionProvider Service Provider."""


from masonite.drivers import QueueAsyncDriver, QueueAmqpDriver
from masonite.managers import QueueManager
from masonite.provider import ServiceProvider
from masonite import Queue
from masonite.helpers import config

class QueueProvider(ServiceProvider):

    wsgi = False

    def register(self):
        from config import queue
        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueAmqpDriver', QueueAmqpDriver)
        self.app.bind('QueueManager', QueueManager)

    def boot(self, queue: QueueManager):
        self.app.bind('Queue', queue.driver(config('queue.driver')))
        self.app.swap(Queue, queue.driver(config('queue.driver')))
