import pendulum


class Task:

    run_every = False
    run_at = False
    run_every_hour = False
    run_every_minute = False
    twice_daily = False
    run_weekly = False

    _date = None

    name = ""

    def __init__(self):
        """
        Should only be on the child class. Also needs to be resolved by the container.
        """

        pass

    def every(self, time):
        self.run_every = time
        return self

    def every_minute(self):
        self.run_every = "1 minute"
        return self

    def every_15_minutes(self):
        self.run_every = "15 minutes"
        return self

    def every_30_minutes(self):
        self.run_every = "30 minutes"
        return self

    def every_45_minutes(self):
        self.run_every = "45 minutes"
        return self

    def hourly(self):
        self.run_every = "1 hour"
        return self

    def daily(self):
        self.run_every = "1 day"
        return self

    def weekly(self):
        self.run_every = "1 week"
        return self

    def monthly(self):
        self.run_every = "1 month"
        return self

    def at(self, run_time):
        self.run_at = run_time
        return self

    def at_twice(self, run_time):
        self.twice_daily = run_time
        return self

    def daily_at(self, run_time):
        return self.daily().at(run_time)

    def handle(self):
        """Fires the task"""

        pass

    def should_run(self, date=None):
        """If the task should run"""

        # set the date
        self._set_date()

        return self._verify_run()

    def _set_date(self):
        if not self._date:
            self._date = pendulum.now()
            if hasattr(self, "timezone"):
                self._date.in_timezone(self.timezone)

    def _verify_run(self):
        if self.run_every:
            length, frequency = self.run_every.split(" ")

            if frequency in ("minute", "minutes"):
                time = int(length)
                if self._date.minute == 0 or self._date.minute % time == 0 or time == 1:
                    return True

            elif frequency in ("hour", "hours"):
                time = int(length)
                if self._date.hour % time == 0 and self._date.minute == 0:
                    return True

            elif frequency in ("day", "days"):
                time = int(length)
                if self._date.day_of_year % time == 0 and (
                    self._date.hour == 0
                    and self._date.minute == 0
                    or self._verify_run_at()
                ):
                    return True
            elif frequency in ("month", "months"):
                time = int(length)
                if (
                    self._date.month % time == 0
                    and self._date.day == 1
                    and (
                        self._date.hour == 0
                        and self._date.minute == 0
                        or (self._date.day == 0 and self._verify_run_at())
                    )
                ):
                    return True

        elif self.run_at:
            return self._verify_run_at()

        if self.run_every_minute:
            return True
        elif self.run_every_hour:
            if self._date.hour / 1 == 1:
                return True
        elif self.twice_daily:
            if self._date.hour in self.twice_daily:
                return True

        return False

    def _verify_run_at(self):
        if self._date.minute < 10:
            minute = f"0{self._date.minute}"
        else:
            minute = self._date.minute

        if f"{self._date.hour}:{minute}" == self.run_at:
            return True

        return False
