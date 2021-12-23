"""This module is overriding ShellCommand to rename to db:shell to make more sense
than shell inside a Masonite project."""
from masoniteorm.commands import ShellCommand


class DbShellCommand(ShellCommand):
    """
    Connect to your database interactive terminal.

    db:shell
        {--c|connection=default : The connection you want to use to connect to interactive terminal}
        {--s|show=? : Display the command which will be called to connect}
    """
