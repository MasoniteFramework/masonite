"""A QueueTableCommand Command"""


from cleo import Command

from ..helpers.filesystem import copy_migration


class QueueTableCommand(Command):
    """
    Create migration files for the queue feature

    queue:table
        {--failed : Created the queue failed table}
        {--jobs : Created the queue failed table}
    """

    def handle(self):
        if self.option("failed"):
            copy_migration("masonite/snippets/migrations/create_failed_jobs_table.py")
            self.info("Failed queue table migration created successfully")
        if self.option("jobs"):
            copy_migration("masonite/snippets/migrations/create_queue_jobs_table.py")
            self.info("Jobs queue table migration created successfully")

        self.line("<error>Please specify the --failed or --jobs flags</error>")
