import os
import sys
from subprocess import check_output

from cleo import Command

from masonite.packages import add_venv_site_packages


class MigrateCommand(Command):
    """
    Run migrations

    migrate
    """

    def handle(self):
        sys.path.append(os.getcwd())
        try:
            add_venv_site_packages()
        except ImportError:
            self.comment('This command must be ran inside of the root of a Masonite project directory')

        from wsgi import container

        migration_directory = ['databases/migrations']
        for key, value in container.providers.items():
            if 'MigrationDirectory' in key:
                migration_directory.append(value)

        for directory in migration_directory:
            self.line('')
            if len(migration_directory) > 1:
                self.info('Migrating: {0}'.format(directory))
            try:
                output = bytes(check_output(
                        ['orator', 'migrate', '-c', 'config/database.py', '-p', directory, '-f']
                    )).decode('utf-8')

                self.line(
                    output.replace('OK', '<info>OK</info>') \
                    .replace('Migrated', '<info>Migrated</info><fg=cyan>') + '</>'
                )
            except Exception:
                pass
