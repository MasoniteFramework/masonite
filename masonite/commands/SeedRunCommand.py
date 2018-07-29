from cleo import Command
import subprocess


class SeedRunCommand(Command):
    """
    Create a seeder to seed a database.

    seed:run
        {table=None : Name of the table to seed}
    """

    def handle(self):
        if not 'sys.path.append(os.getcwd())' in open('databases/seeds/__init__.py').read():
            f = open('databases/seeds/__init__.py', 'w+')
            f.write('import os\nimport sys\nsys.path.append(os.getcwd())\n')
            f.close()

        table = self.argument('table').lower()
        if not table == 'none':
            seeder = '--seeder {}_table_seeder'.format(table.lower())
        else:
            seeder = ''

        subprocess.call([
            "orator db:seed -p databases/seeds -c config/database.py -f {}".format(seeder),
        ], shell=True)
