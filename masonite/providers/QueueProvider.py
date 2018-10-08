""" A RedirectionProvider Service Provider """

from config import queue
from masonite.drivers import QueueAsyncDriver, QueueAmqpDriver
from masonite.managers import QueueManager
from masonite.provider import ServiceProvider


class QueueProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueAmqpDriver', QueueAmqpDriver)
        self.app.bind('QueueManager', QueueManager)
        self.app.bind('QueueConfig', queue)

    def boot(self, QueueConfig, QueueManager):
        self.app.bind(
            'Queue',
            QueueManager(self.app).driver(QueueConfig.DRIVER)
        )
