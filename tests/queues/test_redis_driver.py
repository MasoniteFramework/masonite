from masonite.drivers.QueueRedisDriver import QueueRedisDriver
from masonite.drivers.QueueAsyncDriver import QueueAsyncDriver
from masonite.managers.QueueManager import QueueManager
from masonite.managers.MailManager import MailManager
from masonite.testsuite.TestSuite import TestSuite
from config import queue, mail


def test_redis_driver():
    container = TestSuite().create_container().container

    container.bind('Container', container)
    container.bind('Test', 'Test')
    container.bind('Mail', MailManager(container))
    container.bind('QueueConfig', queue)
    container.bind('QueueRedisDriver', QueueRedisDriver)
    container.bind('QueueAsyncDriver', QueueAsyncDriver)
    container.bind('QueueManager', QueueManager(container))
    container.bind('MailConfig', mail)
    container.bind('MailSmtpDriver', MailManager(container).driver('smtp'))

    manager = container.make('QueueManager').driver('async')
