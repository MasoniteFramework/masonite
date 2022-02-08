from src.masonite.middleware.route.ThrottleRequestsMiddleware import (
    ThrottleRequestsMiddleware,
)
from tests import TestCase
from src.masonite.facades import RateLimiter
from src.masonite.rates import GlobalRate


class TestRateLimiter(TestCase):
    def test_attempts(self):
        self.assertEqual(RateLimiter.attempts("test"), 0)

    # vRateLimiter::for('api', function (Request $request) {
    #         return Limit::perMinute(60)->by(optional($request->user())->id ?: $request->ip());

    def test_register_limiter(self):
        RateLimiter.register("api", GlobalRate("60/min"))
        # route.get("/api/test", "").middleware("throttle:500,1")

    def test_throttle_middleware(self):
        # ThrottleRequestsMiddleware().before(1, 2, 3)
        pass
