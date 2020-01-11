"""Migrate Refresh Command."""

from cleo import Command


class MigrateRefreshCommand(Command):
    """
    Migrate refresh.

    migrate:refresh
        {--s|seed : Seed the database}
        {--c|connection=default : The connection you want to run migrations on}
    """

    def handle(self):
        self.call('migrate:reset', [
            ('--connection', self.option('connection'))
        ])
        self.call('migrate', [
            ('--connection', self.option('connection'))
        ])

        if self.option('seed'):
            self.call('seed:run')
