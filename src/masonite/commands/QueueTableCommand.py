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
        if self.option('failed'):
            copy_migration('masonite/snippets/migrations/create_failed_jobs_table.py')
        if self.option('jobs'):
            copy_migration('masonite/snippets/migrations/create_queue_jobs_table.py')
        self.info('Migration created successfully')
