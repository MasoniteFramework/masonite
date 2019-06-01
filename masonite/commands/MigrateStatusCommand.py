"""Migrate Status Command."""
import os
import sys

from subprocess import check_output
from cleo import Command
from masonite.packages import add_venv_site_packages


class MigrateStatusCommand(Command):
    """
    Migrate status.

    migrate:status
    """

    def handle(self):
        sys.path.append(os.getcwd())
        try:
            add_venv_site_packages()
        except ImportError:
            self.comment(
                'This command must be ran inside of the root of a Masonite project directory')

        from wsgi import container

        migration_directory = ['databases/migrations']
        for key, value in container.providers.items():
            if isinstance(key, str) and 'MigrationDirectory' in key:
                migration_directory.append(value)

        for directory in migration_directory:
            self.line('')
            if len(migration_directory) > 1:
                self.info('Migrate Status: {}'.format(directory))
            try:
                output = bytes(check_output(
                    ['orator', 'migrate:status', '-c',
                        'config/database.py', '-p', directory]
                )).decode('utf-8')

                self.line(
                    output.replace('Yes', '<info>Yes</info>')
                    .replace('No', '<comment>No</comment>'))
            except Exception:
                pass
