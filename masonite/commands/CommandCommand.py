import os
from cleo import Command


class CommandCommand(Command):
    """
    Creates a new command

    command
        {name : Name of the command you would like to create}
    """

    def handle(self):
        command = self.argument('name')
        if not os.path.isfile('app/commands/{0}.py'.format(command)):
            if not os.path.exists(os.path.dirname('app/commands/{0}.py'.format(command))):
                # Create the path to the command if it does not exist
                os.makedirs(os.path.dirname('app/commands/{0}.py'.format(command)))

            f = open('app/commands/{0}.py'.format(command), 'w+')

            f.write('""" A {0} Command """\n'.format(command))
            f.write('from cleo import Command\n\n\n')
            f.write('class {0}(Command):\n    """\n    Description of command\n\n    '.format(command))
            f.write('command:name\n        {argument : description}\n    """\n\n    ')
            f.write('def handle(self):\n        pass')

            self.info('Command Created Successfully!')
        else:
            self.error('Command Already Exists!')
