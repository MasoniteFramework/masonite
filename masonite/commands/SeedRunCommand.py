"""Run Seed Command."""
import subprocess
import os

from cleo import Command


class SeedRunCommand(Command):
    """
    Run seed for database.

    seed:run
        {table=None : Name of the table to seed}
    """

    def handle(self):

        table = self.argument('table').lower()
        if not table == 'none':
            seeder = '--seeder {}_table_seeder'.format(table.lower())
        else:
            seeder = ''

        subprocess.call([
            "orator db:seed -p databases/seeds -c config/database.py -f {}".format(
                seeder),
        ], shell=True)

        self.check_init_file()

    def check_init_file(self):
        os.makedirs(os.path.dirname(
            'databases/seeds/__init__.py'), exist_ok=True)

        with open('databases/seeds/__init__.py') as f:
            if 'sys.path.append(os.getcwd())' not in f.read():
                with open('databases/seeds/__init__.py', 'w+') as fp:
                    fp.write('import os\nimport sys\nsys.path.append(os.getcwd())\n')
