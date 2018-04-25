from cleo import Command
import os
from subprocess import check_output


class MigrateRefreshCommand(Command):
    """
    Migrate refresh

    migrate:refresh
    """

    def handle(self):
        self.call('migrate:reset')
        self.call('migrate')
