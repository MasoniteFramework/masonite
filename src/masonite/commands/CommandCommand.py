"""Creates New Command Command."""
from masonite.commands import BaseScaffoldCommand


class CommandCommand(BaseScaffoldCommand):
    """
    Creates a new command.

    command
        {name : Name of the command you would like to create}
    """

    scaffold_name = 'Command'
    postfix = "Command"
    template = '/masonite/snippets/scaffold/command'
    base_directory = 'app/commands/'
