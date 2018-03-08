""" A RedirectionProvider Service Provider """
from masonite.provider import ServiceProvider
from masonite.drivers.QueueAsyncDriver import QueueAsyncDriver
from masonite.managers.QueueManager import QueueManager
from config import queue


class QueueProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('QueueAsyncDriver', QueueAsyncDriver)
        self.app.bind('QueueManager', QueueManager)
        self.app.bind('QueueConfig', queue)

    def boot(self, QueueConfig, QueueManager):
        self.app.bind(
            'Queue',
            QueueManager(self.app).driver(QueueConfig.DRIVER)
        )
