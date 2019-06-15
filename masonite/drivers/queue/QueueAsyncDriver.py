"""Async Driver Method."""

import inspect
import os

from masonite.app import App
from masonite.contracts import QueueContract
from masonite.drivers import BaseQueueDriver
from masonite.exceptions import QueueException
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from masonite.helpers import config


class QueueAsyncDriver(BaseQueueDriver, QueueContract):
    """Queue Aysnc Driver."""

    def __init__(self, app: App):
        """Queue Async Driver.

        Arguments:
            Container {masonite.app.App} -- The application container.
        """
        self.container = app

    def _get_processor(self, mode, max_workers):
        """Set processor to use either threads or multiprocesses

        Arguments:
            mode {str} - async mode
            max_workers {int} - number of threads/processes to use
        """

        # Necessary for Python 3.4, can be removed in 3.5+
        if max_workers is None:
            # Use this number because ThreadPoolExecutor is often
            # used to overlap I/O instead of CPU work.
            max_workers = (os.cpu_count() or 1) * 5
        if max_workers <= 0:
            raise QueueException("max_workers must be greater than 0")

        # Determine Mode for Processing
        if mode == 'threading':
            processor = ThreadPoolExecutor(max_workers)
        elif mode == 'multiprocess':
            processor = ProcessPoolExecutor(max_workers)
        else:
            raise QueueException('Queue mode {} not recognized'.format(mode))
        return processor

    def push(self, *objects, args=(), kwargs={}, **options):
        """Push objects onto the async stack.

        Arguments:
            objects {*args of objects} - This can be several objects as parameters into this method.
            options {**kwargs of options} - Additional options for async driver
        """

        # Initialize Extra Options
        callback = options.get('callback', 'handle')
        mode = options.get('mode', config('queue.drivers.async.mode', 'threading'))
        workers = options.get('workers', None)

        # Set processor to either use threads or processes
        processsor = self._get_processor(mode=mode, max_workers=workers)

        with processsor as executor:
            for obj in objects:
                obj = self.container.resolve(obj) if inspect.isclass(obj) else obj
                try:
                    executor.submit(
                        fn=getattr(obj, callback), args=args, kwargs=kwargs)
                except AttributeError:
                    # Could be wanting to call only a method asyncronously
                    executor.submit(fn=obj, args=args, kwargs=kwargs)
