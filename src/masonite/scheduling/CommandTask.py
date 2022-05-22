# @M5 remove or document this unused class

import subprocess

from .Task import Task


class CommandTask(Task):

    run_every_minute = True

    def __init__(self, command: str = ""):
        self.command = command

    def handle(self):
        subprocess.call(self.command.split(" "))
