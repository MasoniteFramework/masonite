"""Async Driver Method."""

import inspect
import threading

from masonite.app import App
from masonite.contracts import QueueContract
from masonite.drivers import BaseQueueDriver
from masonite.exceptions import QueueException
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

class QueueAsyncDriver(BaseQueueDriver, QueueContract):
    """Queue Aysnc Driver."""

    def __init__(self, app: App):
        """Queue Async Driver.

        Arguments:
            Container {masonite.app.App} -- The application container.
        """
        self.container = app


    def _threading(self):
        """ Implements Async by Threading """

        with ThreadPoolExecutor(max_workers = self.workers) as executor:
            for obj in self.objects:
                if inspect.isclass(obj):
                    obj = self.container.resolve(obj)

                try:
                    executor.submit(
                        fn=getattr(obj, self.callback), args=self.args, kwargs=self.kwargs)
                except AttributeError:
                    # Could be wanting to call only a method asyncronously
                    executor.submit(fn=obj, args=self.args, kwargs=self.kwargs)

    def _multiprocessing(self):
        """ Implements Async by Multiprocesses """

        with ProcessPoolExecutor(max_workers = self.workers) as executor:
            for obj in self.objects:
                if inspect.isclass(obj):
                    obj = self.container.resolve(obj)

                try:
                    executor.submit(
                        fn=getattr(obj, self.callback), args=self.args, kwargs=self.kwargs)
                except AttributeError:
                    # Could be wanting to call only a method asyncronously
                    executor.submit(fn=obj, args=self.args, kwargs=self.kwargs)

    def push(self, *objects, args=(), kwargs={}, callback='handle', mode='threading', workers=None):
        """Push objects onto the async stack.

        Arguments:
            objects {*args of objects} - This can be several objects as parameters into this method.
        """

        self.workers = workers
        self.objects = objects
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        if mode == 'threading':
            self._threading()
        elif mode == 'multiprocess':
            self._multiprocessing()
        else:
            raise QueueException('Queue mode {} not recognized'.format(mode))
