import os
from cleo import Command
from masonite.view import View
from masonite.app import App
from masonite.helpers.filesystem import make_directory


class CommandCommand(Command):
    """
    Creates a new command

    command
        {name : Name of the command you would like to create}
    """

    def handle(self):
        command = self.argument('name')
        view = View(App())
        command_directory = 'app/commands/{0}.py'.format(command)

        if not make_directory(command_directory):
            return self.error('Command Already Exists!')

        f = open('app/commands/{0}.py'.format(command), 'w+')
        if view.exists('/masonite/snippets/scaffold/model'):
            f.write(
                view.render('/masonite/snippets/scaffold/command',
                            {'class': command.split('/')[-1]}).rendered_template
            )
            self.info('Command Created Successfully!')
            return f.close()
