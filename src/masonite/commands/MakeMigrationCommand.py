"""New Migration Command."""
import subprocess

from cleo import Command


class MakeMigrationCommand(Command):
    """
    Makes a new migration.

    migration
        {name : Name of your migration}
        {--t|--table=False : Table you are migrating for}
        {--c|--create=False : Table you want to create with this migration}
    """

    def handle(self):
        name = self.argument('name')

        if self.option('create') != 'False':
            subprocess.call(['orator', 'make:migration', name,
                             '-p', 'databases/migrations', '--table', self.option('create'), '--create'])
        elif self.option('table') != 'False':
            subprocess.call(['orator', 'make:migration', name,
                             '-p', 'databases/migrations', '--table', self.option('table')])
        else:
            subprocess.call(['orator', 'make:migration', name,
                             '-p', 'databases/migrations'])
