import inspect
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING

from ...exceptions import QueueException

if TYPE_CHECKING:
    from ...foundation import Application
    from ...queues import Queueable


class AsyncDriver:
    def __init__(self, application: "Application"):
        self.application = application

    def set_options(self, options: dict) -> "AsyncDriver":
        self.options = options
        return self

    def push(self, *jobs: "Queueable", args=(), **kwargs) -> None:
        """Push objects onto the async stack.

        Arguments:
            objects {*args of objects} - This can be several objects as parameters into this method.
            options {**kwargs of options} - Additional options for async driver
        """

        # Initialize Extra Options
        options = self.options
        callback = options.get("callback", "handle")
        mode = options.get("mode", "threading")
        workers = options.get("workers", None)

        # Set processor to either use threads or processes
        processor = self._get_processor(mode=mode, max_workers=workers)
        is_blocking = options.get("blocking", False)

        ran = {}
        for obj in jobs:
            obj = self.application.resolve(obj) if inspect.isclass(obj) else obj
            try:
                future = processor.submit(getattr(obj, callback), *args, **kwargs)
            except AttributeError:
                # Could be wanting to call only a method asynchronously
                future = processor.submit(obj, *args, **kwargs)
            ran.update({future: obj})

        if is_blocking:
            for job in as_completed(ran.keys()):
                if job.exception():
                    ran[job].failed(ran[job], job.exception())
                print(f"Job Ran: {job}")

    def consume(self, **options) -> None:
        pass

    def retry(self, **options) -> None:
        pass

    def _get_processor(
        self, mode: str, max_workers: int
    ) -> "ThreadPoolExecutor|ProcessPoolExecutor":
        """Set processor to use either 'threading' or 'multiprocess' mode. Max number of
        threads/processes should also be specified."""

        if max_workers is None:
            # Use this number because ThreadPoolExecutor is often
            # used to overlap I/O instead of CPU work.
            max_workers = (os.cpu_count() or 1) * 5

        # Determine Mode for Processing
        if mode == "threading":
            processor = ThreadPoolExecutor(max_workers)
        elif mode == "multiprocess":
            processor = ProcessPoolExecutor(max_workers)
        else:
            raise QueueException("Queue mode {} not recognized".format(mode))
        return processor
