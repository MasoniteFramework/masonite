from .Task import Task
import subprocess


class CommandTask(Task):

    run_every_minute = True

    def __init__(self, command=""):
        self.command = command

    def handle(self):
        subprocess.call(self.command.split(" "))
