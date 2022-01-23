""" A ScheduleRunCommand Command """
from cleo import Command


class ScheduleRunCommand(Command):
    """
    Run the scheduled tasks
    schedule:run
        {--t|task=? : Name of task you want to run (else all scheduled tasks will be ran)}
        {--f|force : Force running task immediately}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        return self.app.make("scheduler").run(
            run_name=self.option("task"), force=self.option("force")
        )
