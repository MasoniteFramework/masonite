"""Queue Failed Command."""
import os

from ..utils.filesystem import make_directory, get_module_dir
from ..utils.time import migration_timestamp
from ..utils.location import base_path
from .Command import Command


class QueueFailedCommand(Command):
    """
    Creates a failed jobs table

    queue:failed
        {--d|--directory=databases/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        with open(
            os.path.join(
                get_module_dir(__file__), "../stubs/queue/create_failed_jobs_table.py"
            )
        ) as fp:
            output = fp.read()

        filename = f"{migration_timestamp()}_create_failed_jobs_table.py"
        path = os.path.join(base_path(self.option("directory")), filename)
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {filename}")
