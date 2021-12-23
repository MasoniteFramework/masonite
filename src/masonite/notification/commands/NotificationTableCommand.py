"""Notification Table Command."""
from cleo import Command
import os

from ...utils.filesystem import get_module_dir, make_directory
from ...utils.time import migration_timestamp
from ...utils.location import base_path


class NotificationTableCommand(Command):
    """
    Creates the notifications table needed for storing notifications in the database.

    notification:table
        {--d|--directory=databases/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        with open(
            os.path.join(
                get_module_dir(__file__),
                "../../stubs/notification/create_notifications_table.py",
            )
        ) as fp:
            output = fp.read()

        relative_filename = os.path.join(
            self.option("directory"),
            f"{migration_timestamp()}_create_notifications_table.py",
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {relative_filename}")
