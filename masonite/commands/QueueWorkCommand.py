""" A QueueWorkCommand Command """

import inspect
import pickle

from cleo import Command

from masonite import Queue
from masonite.exceptions import DriverLibraryNotFound


class QueueWorkCommand(Command):
    """
    Start the queue worker

    queue:work
        {--c|channel=default : The channel to listen on the queue}
        {--d|driver=default : Specify the driver you would like to connect to}
        {--f|fair : Send jobs to queues that have no jobs instead of randomly selecting a queue}
        {--failed : Run only the failed jobs}
    """

    def handle(self):
        from wsgi import container

        if self.option('driver') == 'default':
            queue = container.make(Queue)
        else:
            queue = container.make(Queue).driver(self.option('driver'))

        if self.option('failed'):
            queue.run_failed_jobs()
            return

        queue.connect().consume(self.option('channel'), fair=self.option('fair'))
