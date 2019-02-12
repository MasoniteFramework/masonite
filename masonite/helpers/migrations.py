import subprocess
from masonite.helpers import config


def has_unmigrated_migrations():
    if not config('application.debug'):
        return False

    from wsgi import container
    from config.database import DB
    try:
        DB.connection()
    except Exception:
        return False

    migration_directory = ['databases/migrations']
    for key, value in container.providers.items():
        if type(key) == str and 'MigrationDirectory' in key:
            migration_directory.append(value)

    for directory in migration_directory:
        try:
            output = bytes(subprocess.check_output(
                ['orator', 'migrate:status', '-c',
                    'config/database.py', '-p', directory]
            )).decode('utf-8')

            if 'No' in output:
                return True
        except Exception:
            pass

    return False
