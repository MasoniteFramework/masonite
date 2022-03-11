import sys
from tests import TestCase

from src.masonite.rates import UnlimitedLimiter, GlobalLimiter, Limit, GuestsOnlyLimiter
from tests.integrations.app.User import User


class TestLimits(TestCase):
    def test_limit_from_str(self):
        limit = Limit.from_str("10/hour")
        assert limit.max_attempts == 10
        assert limit.delay == 60

    def test_limit_per_minute(self):
        limit = Limit.per_minute(5)
        assert limit.max_attempts == 5
        assert limit.delay == 1

    def test_limit_per_hour(self):
        limit = Limit.per_hour(10)
        assert limit.max_attempts == 10
        assert limit.delay == 60

    def test_limit_per_day(self):
        limit = Limit.per_day(10)
        assert limit.max_attempts == 10
        assert limit.delay == 60 * 24

    def test_limit_custom(self):
        limit = Limit(500, 40)
        assert limit.max_attempts == 500
        assert limit.delay == 40

    def test_limit_unlimited(self):
        limit = Limit.unlimited()
        assert limit.max_attempts == sys.maxsize
        assert limit.is_unlimited()


class TestLimiters(TestCase):
    def test_unlimited(self):
        request = "fake"
        limiter = UnlimitedLimiter()
        limit = limiter.allow(request)
        assert limit.is_unlimited()
        assert limit.max_attempts == sys.maxsize

    def test_global(self):
        request = "fake"
        limiter = GlobalLimiter("3/minute")
        limit = limiter.allow(request)
        assert not limit.is_unlimited()
        assert limit.max_attempts == 3
        assert limit.delay == 1
        limiter = GlobalLimiter("100/day")
        limit = limiter.allow(request)
        assert not limit.is_unlimited()
        assert limit.max_attempts == 100
        assert limit.delay == 24 * 60

    def test_guests_only(self):
        # request as guest
        request = self.make_request()
        request._ip = "127.0.0.1"

        limiter = GuestsOnlyLimiter("2/hour")
        limit = limiter.allow(request)
        assert not limit.is_unlimited()
        assert limit.max_attempts == 2
        assert limit.delay == 60
        assert limit.key == "127.0.0.1"

        request._ip = "192.168.0.1"
        limit = limiter.allow(request)
        assert limit.key == "192.168.0.1"

    def test_guests_only_with_authenticated_user(self):
        limiter = GuestsOnlyLimiter("2/hour")
        user = User.find(1)
        # request as authenticated user
        request = self.make_request()
        request.set_user(user)
        limit = limiter.allow(request)
        assert limit.is_unlimited()
