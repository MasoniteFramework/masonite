""" Async Driver Method """

import threading

from masonite.contracts.QueueContract import QueueContract
from masonite.drivers.BaseDriver import BaseDriver


class QueueAsyncDriver(QueueContract, BaseDriver):
    """Queue Aysnc Driver
    """

    def __init__(self, Container):
        """Queue Async Driver

        Arguments:
            Container {masonite.app.App} -- The application container.
        """

        self.container = Container

    def push(self, *objects):
        """Push objects onto the async stack.

        Arguments:
            objects {*args of objects} - This can be several objects as parameters into this method.
        """

        for obj in objects:
            obj = self.container.resolve(obj)
            thread = threading.Thread(
                target=obj.dispatch(), args=(), kwargs={})
            thread.start()
