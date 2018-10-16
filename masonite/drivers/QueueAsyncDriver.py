"""Async Driver Method."""

import threading
import inspect

from masonite.contracts import QueueContract
from masonite.drivers import BaseDriver
from masonite.app import App


class QueueAsyncDriver(QueueContract, BaseDriver):
    """Queue Aysnc Driver."""

    def __init__(self, app: App):
        """Queue Async Driver.

        Arguments:
            Container {masonite.app.App} -- The application container.
        """
        self.container = app

    def push(self, *objects, args=()):
        """Push objects onto the async stack.

        Arguments:
            objects {*args of objects} - This can be several objects as parameters into this method.
        """
        for obj in objects:
            if inspect.isclass(obj):
                obj = self.container.resolve(obj)

            thread = threading.Thread(
                target=obj.handle, args=args, kwargs={})
            thread.start()
