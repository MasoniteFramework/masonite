from ...providers import Provider
from ..commands import MakeTaskCommand, ScheduleRunCommand
from ..TaskHandler import TaskHandler


class ScheduleProvider(Provider):
    """ScheduleProvider adding scheduling feature to the project."""

    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make("commands").add(
            MakeTaskCommand(self.application), ScheduleRunCommand(self.application)
        )

        self.application.bind("scheduler", TaskHandler(self.application))

    def boot(self):
        pass
