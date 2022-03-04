"""Task Module Description"""
from src.masonite.scheduling import Task


class TaskTest(Task):

    name = "task_test"

    def handle(self):
        print("executed")
