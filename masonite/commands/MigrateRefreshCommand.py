"""Migrate Refresh Command."""

from cleo import Command


class MigrateRefreshCommand(Command):
    """
    Migrate refresh.

    migrate:refresh
        {--s|seed : Seed the database}
    """

    def handle(self):
        self.call('migrate:reset')
        self.call('migrate')

        if self.option('seed'):
            self.call('seed:run')
