"""Queue Retry Command."""
from .Command import Command


class QueueRetryCommand(Command):
    """
    Puts all failed queue jobs back onto the queue.

    queue:retry
        {--c|--connection=default : Specifies the database connection if using database driver.}
        {--queue=default : The queue to listen to}
        {--d|driver=None : Specify the driver you would like to connect to}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        driver = None if self.option("driver") == "None" else self.option("driver")

        return self.app.make("queue").retry(
            {
                "driver": driver,
                "connection": self.option("connection"),
                "queue": self.option("queue"),
            }
        )
