from tests import TestCase
from src.masonite.facades import Rate
from src.masonite.rates import Limit


class TestRateLimiter(TestCase):
    def test_attempts(self):
        self.assertEqual(Rate.attempts("test"), 0)

    # vRateLimiter::for('api', function (Request $request) {
    #         return Limit::perMinute(60)->by(optional($request->user())->id ?: $request->ip());

    def test_register_limiter(self):
        Rate.register("api", lambda request: Limit.per_minute(60).by(request.ip()))
