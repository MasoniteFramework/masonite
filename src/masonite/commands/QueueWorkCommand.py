"""A QueueWorkCommand Command."""

from cleo import Command

from .. import Queue


class QueueWorkCommand(Command):
    """
    Start the queue worker

    queue:work
        {--c|channel=default : The channel to listen on the queue}
        {--queue=default : The queue to listen to}
        {--d|driver=default : Specify the driver you would like to connect to}
        {--f|fair : Send jobs to queues that have no jobs instead of randomly selecting a queue}
        {--p|poll=0 : Specify the amount of time a worker should poll}
        {--failed : Run only the failed jobs}
    """

    def handle(self):
        from wsgi import container

        if self.option("driver") == "default":
            queue = container.make(Queue)
        else:
            queue = container.make(Queue).driver(self.option("driver"))

        if self.option("failed"):
            queue.run_failed_jobs()
            return

        queue.connect().consume(
            self.option("channel"),
            fair=self.option("fair"),
            poll=self.option("poll"),
            queue=self.option("queue"),
        )
