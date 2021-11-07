import pytest
import pendulum
from src.masonite.scheduling import TaskHandler, Task
from tests import TestCase


class MockTask1(Task):
    run_every = "1 minutes"
    timezone = "America/New_York"

    def handle(self):
        print("hello 1")


class MockTask2(Task):
    run_every = "1 minutes"
    timezone = "America/New_York"

    def handle(self):
        print("hello 2")


class TestHandler(TestCase):
    def test_handler_adds_and_runs_tasks(self):
        self.handler = TaskHandler(self.application)
        self.handler.add(MockTask1, MockTask2())
        self.handler.run()
