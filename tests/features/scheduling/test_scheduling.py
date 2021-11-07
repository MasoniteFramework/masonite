import pytest
import pendulum
from src.masonite.scheduling import Task


class MockTask(Task):
    run_every = "5 minutes"
    timezone = "America/New_York"


class TestScheduler:
    def setup_method(self):
        self.task = MockTask()

    def test_scheduler_should_run(self):
        assert self.task.run_every == "5 minutes"
        time = pendulum.now().on(2018, 5, 21).at(22, 5, 5)
        self.task._date = time
        assert self.task.should_run(time) == True

        time = pendulum.now().on(2018, 5, 21).at(22, 6, 5)
        self.task._date = time
        assert self.task.should_run(time) == False

    def test_scheduler_should_run_every_minute(self):
        self.task.run_every = "1 minute"
        time = pendulum.now().on(2018, 5, 21).at(22, 5, 5)
        self.task._date = time
        assert self.task.should_run(time) == True

        time = pendulum.now().on(2018, 5, 21).at(22, 6, 5)
        self.task._date = time
        assert self.task.should_run(time) == True

    def test_scheduler_should_run_every_2_minutes(self):
        self.task.run_every = "2 minutes"
        time = pendulum.now().on(2018, 5, 21).at(14, 56, 5)
        self.task._date = time
        assert self.task.should_run(time) == True

        time = pendulum.now().on(2018, 5, 21).at(14, 58, 5)
        self.task._date = time
        assert self.task.should_run(time) == True

    def test_scheduler_should_run_every_hour(self):
        self.task.run_every = "1 hour"
        time = pendulum.now().on(2018, 5, 21).at(2, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == True

        time = pendulum.now().on(2018, 5, 21).at(3, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == True

        self.task.run_every = "2 hours"
        time = pendulum.now().on(2018, 5, 21).at(2, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == True

        self.task.run_every = "2 hours"
        time = pendulum.now().on(2018, 5, 21).at(3, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == False

        time = pendulum.now().on(2018, 5, 21).at(4, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == True

    def test_scheduler_should_run_every_days(self):
        self.task.run_every = "2 days"
        time = pendulum.now().on(2018, 5, 21).at(0, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == False

        time = pendulum.now().on(2018, 5, 23).at(0, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == False

        self.task.run_at = "5:30"
        time = pendulum.now().on(2018, 5, 22).at(5, 30, 0)
        self.task._date = time
        assert self.task.should_run(time) == True

        self.task.run_at = "5:35"
        time = pendulum.now().on(2018, 5, 22).at(5, 30, 0)
        self.task._date = time
        assert self.task.should_run(time) == False

    def test_scheduler_should_run_every_months(self):
        self.task.run_every = "2 months"
        time = pendulum.now().on(2018, 1, 1).at(0, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == False

        time = pendulum.now().on(2018, 2, 1).at(0, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == True

        time = pendulum.now().on(2018, 2, 1).at(10, 0, 1)
        self.task._date = time
        assert self.task.should_run(time) == False

        self.task.run_at = "5:30"
        time = pendulum.now().on(2018, 2, 1).at(5, 30, 0)
        self.task._date = time
        assert self.task.should_run(time) == False

    def test_twice_daily_at_correct_time(self):
        time = pendulum.now().on(2018, 1, 1).at(1, 20, 5)
        self.task.run_every = ""
        self.task.twice_daily = (1, 13)
        self.task._date = time

        assert self.task.should_run()

        time = pendulum.now().on(2018, 1, 1).at(13, 20, 5)
        self.task._date = time
        assert self.task.should_run()

    def test_twice_daily_at_incorrect_time(self):
        time = pendulum.now().on(2018, 1, 1).at(12, 20, 5)
        self.task.run_every = ""
        self.task.twice_daily = (1, 13)
        self.task._date = time

        assert self.task.should_run() is False

    def test_run_at(self):
        self.task.run_every = ""
        self.task.run_at = "13:00"

        time = pendulum.now().on(2018, 1, 1).at(13, 0, 5)
        self.task._date = time

        self.task.run_at = "13:05"

        time = pendulum.now().on(2018, 1, 1).at(13, 5, 5)
        self.task._date = time

        assert self.task.should_run() is True

        time = pendulum.now().on(2018, 1, 1).at(13, 6, 5)
        self.task._date = time

        assert self.task.should_run() is False

    def test_method_calls(self):
        task = MockTask()
        task.at("13:00")

        time = pendulum.now().on(2018, 1, 1).at(13, 0, 5)
        task._date = time

        assert task.should_run(time) == True

        task = MockTask()
        task.every_minute()

        time = pendulum.now().on(2018, 5, 21).at(22, 5, 5)
        task._date = time
        assert task.should_run(time) == True
