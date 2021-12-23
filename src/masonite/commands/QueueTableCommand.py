"""New Queue Table Command."""
import os

from ..utils.filesystem import make_directory, get_module_dir
from ..utils.time import migration_timestamp
from ..utils.location import base_path
from .Command import Command


class QueueTableCommand(Command):
    """
    Creates the jobs table

    queue:table
        {--d|--directory=databases/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        with open(
            os.path.join(
                get_module_dir(__file__), "../stubs/queue/create_queue_jobs_table.py"
            )
        ) as fp:
            output = fp.read()

        relative_filename = os.path.join(
            self.option("directory"),
            f"{migration_timestamp()}_create_queue_jobs_table.py",
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {relative_filename}")
