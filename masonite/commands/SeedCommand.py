"""New Seeder Command."""
import subprocess
import os

from cleo import Command


class SeedCommand(Command):
    """
    Create a seeder to seed a database.

    seed
        {table : Name of the table to seed}
    """

    def handle(self):
        table = self.argument('table').lower()
        subprocess.call([
            "orator make:seed {}_table_seeder -p databases/seeds".format(
                table),
        ], shell=True)

        self.check_init_file()

    def check_init_file(self):
        os.makedirs(os.path.dirname(
            'databases/seeds/__init__.py'), exist_ok=True)

        if 'sys.path.append(os.getcwd())' not in open('databases/seeds/__init__.py').read():
            f = open('databases/seeds/__init__.py', 'w+')
            f.write('import os\nimport sys\nsys.path.append(os.getcwd())\n')
            f.close()
