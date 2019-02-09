""" A QueueTableCommand Command """


from cleo import Command

from masonite.helpers.filesystem import copy_migration


class QueueTableCommand(Command):
    """
    Create migration files for the queue feature

    queue:table
    """

    def handle(self):
        copy_migration('masonite/snippets/migrations/create_failed_jobs_table.py')
        self.info('Migration created successfully')
