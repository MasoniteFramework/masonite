class CanSchedule:
    def call(self, command):
        command_class = CommandTask(command)
        self.app.make("scheduler").add(command_class)
        return command_class

    def schedule(self, task):
        task_class = task
        self.app.make("scheduler").add(task_class)
        return task_class
