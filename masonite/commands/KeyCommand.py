"""New Key Command."""
from cleo import Command
from cryptography.fernet import Fernet


class KeyCommand(Command):
    """
    Generate a new key.

    key
        {--s|--store : Stores the key in the .env file}
    """

    def handle(self):
        store = self.option('store')
        key = bytes(Fernet.generate_key()).decode('utf-8')

        if store:
            with open('.env', 'r') as file:
                # read a list of lines into data
                data = file.readlines()

            # change the line that starts with KEY=
            for line_number, line in enumerate(data):
                if line.startswith('KEY='):
                    data[line_number] = 'KEY={}\n'.format(key)
                    break

            # and write everything back
            with open('.env', 'w') as file:
                file.writelines(data)

            self.info('Key added to your .env file: {}'.format(key))
        else:
            self.info("Key: {}".format(key))
