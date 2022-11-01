import inspect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..foundation import Application
    from .Task import Task


class TaskHandler:
    def __init__(self, application: "Application", tasks: "Task" = []):
        self.tasks = tasks
        self.application = application

    def add(self, *tasks: "Task"):
        self.tasks += list(tasks)

    def run(self, run_name: str = None, force: bool = False) -> None:
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
