"""Queue Work Command."""
from .Command import Command


class QueueWorkCommand(Command):
    """
    Creates a new queue worker to consume queue jobs

    queue:work
        {--c|--connection : Specifies the database connection if using database driver.}
        {--queue=? : The queue to listen to}
        {--d|driver=? : Specify the driver you would like to use}
        {--p|poll=? : Specify the seconds a worker should wait before fetching new jobs}
        {--attempts=? : Specify the number of times a job should be retried before it fails}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        options = {}
        options.update({"driver": self.option("driver")})
        options.update({"poll": self.option("poll") or "1"})
        options.update({"attempts": self.option("attempts") or "3"})
        options.update({"queue": self.option("queue") or "default"})

        if self.option("verbose"):
            options.update({"verbosity": "v" + self.option("verbose")})

        return self.app.make("queue").consume(options)
