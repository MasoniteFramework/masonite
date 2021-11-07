from ..drivers.queue import DatabaseDriver, AsyncDriver, AMQPDriver
from ..queues import Queue
from ..configuration import config


class QueueProvider:
    def __init__(self, application):
        self.application = application

    def register(self):
        queue = Queue(self.application).set_configuration(config("queue.drivers"))
        queue.add_driver("database", DatabaseDriver(self.application))
        queue.add_driver("async", AsyncDriver(self.application))
        queue.add_driver("amqp", AMQPDriver(self.application))
        self.application.bind("queue", queue)

    def boot(self):
        pass
