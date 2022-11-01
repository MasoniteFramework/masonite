# @M5 remove or fix and document this unused class
class CanSchedule:
    def call(self, command: str):
        command_class = CommandTask(command)
        self.app.make("scheduler").add(command_class)
        return command_class

    def schedule(self, task):
        task_class = task
        self.app.make("scheduler").add(task_class)
        return task_class
