import pendulum
from tests import TestCase

from src.masonite.facades import RateLimiter, Cache


def my_function():
    return "done"


class TestRateLimiter(TestCase):
    def tearDown(self):
        super().tearDown()
        # delete cache entries between tests for idempotent tests
        self.application.make("cache").store().flush()
        # always restore time if it has been faked
        self.restoreTime()

    def test_attempt(self):
        self.assertEqual(RateLimiter.attempt("test_attempt", my_function, 2), "done")
        self.assertEqual(RateLimiter.attempt("test_attempt", my_function, 2), "done")
        self.assertEqual(RateLimiter.attempt("test_attempt", my_function, 2), False)

    def test_clear_remove_cache_keys(self):
        RateLimiter.attempt("test_key", my_function, 2)
        assert Cache.store().has("test_key")
        assert Cache.store().has("test_key:timer")
        RateLimiter.clear("test_key")
        assert not Cache.store().has("test_key:timer")
        assert not Cache.store().has("test_key")

    def test_reset_attempts(self):
        RateLimiter.attempt("test_key", my_function, 2)
        assert Cache.store().get("test_key") == "1"
        RateLimiter.reset_attempts("test_key")
        assert Cache.store().get("test_key") == "0"

    def test_attempts(self):
        RateLimiter.attempt("test_key", my_function, 2)
        RateLimiter.attempt("test_key", my_function, 2)
        assert RateLimiter.attempts("test_key") == 2

    def test_remaining(self):
        RateLimiter.attempt("test_key", my_function, 2)
        assert RateLimiter.remaining("test_key", 2) == 1

    def test_hit(self):
        now = pendulum.now()
        self.fakeTime(now)
        should_be_available_at = now.add(seconds=40)
        RateLimiter.hit("test_key", 40)
        assert Cache.store().get("test_key") == "1"
        assert Cache.store().get("test_key:timer") == str(
            should_be_available_at.int_timestamp
        )

    def test_available_at(self):
        now = pendulum.now()
        self.fakeTime(now)
        should_be_available_at = now.add(seconds=40)
        RateLimiter.hit("test_key", 40)
        assert (
            RateLimiter.available_at("test_key") == should_be_available_at.int_timestamp
        )
