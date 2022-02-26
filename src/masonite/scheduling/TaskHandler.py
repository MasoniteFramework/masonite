import inspect


class TaskHandler:
    def __init__(self, application, tasks=None):
        if tasks is None:
            tasks = []

        self.tasks = tasks
        self.application = application

    def add(self, *tasks):
        self.tasks += list(tasks)

    def run(self, run_name=None, force=False):
        app = self.application
        for task_class in self.tasks:
            # Resolve the task with the container
            task_identifier = [task_class.name, task_class.__class__.__name__]
            if run_name and run_name not in task_identifier:
                continue

            if inspect.isclass(task_class):
                task = app.resolve(task_class)
            else:
                task = task_class

            # If the class should run then run it
            if task.should_run() or force:
                task.handle()
