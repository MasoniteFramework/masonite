from cleo import Command


class MigrateRefreshCommand(Command):
    """
    Migrate refresh

    migrate:refresh
    """

    def handle(self):
        self.call('migrate:reset')
        self.call('migrate')
