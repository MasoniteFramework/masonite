import pendulum
from tests import TestCase

from src.masonite.utils.time import (
    migration_timestamp,
    parse_human_time,
    cookie_expire_time,
)


class TestTimeUtils(TestCase):
    def tearDown(self):
        super().tearDown()
        self.restoreTime()

    def test_parse_human_time_now(self):
        ref_time = pendulum.datetime(2021, 1, 1)
        self.fakeTime(ref_time)
        instance = parse_human_time("now")
        self.assertEqual(ref_time, instance)

    def test_parse_human_time_expired(self):
        self.fakeTime(pendulum.datetime(2021, 1, 1))
        instance = parse_human_time("expired")
        self.assertEqual(pendulum.datetime(2001, 1, 1), instance)

    def test_parse_human_time(self):
        self.fakeTime(pendulum.datetime(2021, 1, 1, 12, 0, 0))
        self.assertEqual(
            pendulum.datetime(2021, 1, 1, 12, 0, 2), parse_human_time("2 seconds")
        )
        self.assertEqual(
            pendulum.datetime(2021, 1, 1, 12, 2, 0), parse_human_time("2 minutes")
        )
        self.assertEqual(
            pendulum.datetime(2021, 1, 1, 14, 0, 0), parse_human_time("2 hour")
        )
        self.assertEqual(
            pendulum.datetime(2021, 1, 2, 12, 0, 0), parse_human_time("1 day")
        )
        self.assertEqual(
            pendulum.datetime(2021, 1, 15, 12, 0, 0), parse_human_time("2 weeks")
        )
        self.assertEqual(
            pendulum.datetime(2021, 4, 1, 12, 0, 0), parse_human_time("3 months")
        )
        self.assertEqual(
            pendulum.datetime(2030, 1, 1, 12, 0, 0), parse_human_time("9 years")
        )

        self.assertEqual(None, parse_human_time("10 nanoseconds"))

    def test_cookie_expire_time(self):
        self.fakeTime(pendulum.datetime(2021, 1, 21, 7, 28, 0))
        expiration_time_str = cookie_expire_time("7 days")
        self.assertEqual(expiration_time_str, "Thu, 28 Jan 2021 07:28:00")

    def test_migration_timestamp(self):
        self.fakeTime(pendulum.datetime(2021, 10, 25, 8, 12, 54))
        self.assertEqual(migration_timestamp(), "2021_10_25_081254")
