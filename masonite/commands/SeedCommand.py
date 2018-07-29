from cleo import Command
import subprocess


class SeedCommand(Command):
    """
    Create a seeder to seed a database.

    seed
        {table : Name of the table to seed}
    """

    def handle(self):
        if not 'sys.path.append(os.getcwd())' in open('databases/seeds/__init__.py').read():
            f = open('databases/seeds/__init__.py', 'w+')
            f.write('import os\nimport sys\nsys.path.append(os.getcwd())\n')
            f.close()

        table = self.argument('table').lower()
        subprocess.call([
            "orator make:seed {}_table_seeder -p databases/seeds".format(table),
        ], shell=True)


