""" A ScheduleRunCommand Command """
import pendulum
import inspect
from cleo import Command

from ..Task import Task


class ScheduleRunCommand(Command):
    """
    Run the scheduled tasks
    schedule:run
        {--t|task=None : Name of task you want to run}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        return self.app.make("scheduler").run()
