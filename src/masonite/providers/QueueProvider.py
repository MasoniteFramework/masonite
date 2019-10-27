"""A RedirectionProvider Service Provider."""


from ..drivers import QueueAsyncDriver, QueueAmqpDriver
from ..managers import QueueManager
from ..provider import ServiceProvider
from .. import Queue
from ..helpers import config


class QueueProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueAmqpDriver', QueueAmqpDriver)
        self.app.bind('QueueManager', QueueManager)

    def boot(self, queue: QueueManager):
        self.app.bind('Queue', queue.driver(config('queue.driver')))
        self.app.swap(Queue, queue.driver(config('queue.driver')))
