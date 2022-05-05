from tests import TestCase

from src.masonite.rates import GlobalLimiter, GuestsOnlyLimiter, Limiter, Limit
from src.masonite.routes import Route
from src.masonite.facades import RateLimiter
from src.masonite.exceptions import ThrottleRequestsException
from tests.integrations.app.User import User


class CustomLimit(Limiter):
    def allow(self, request):
        return Limit.per_day(2)

    def get_response(self, request, response, headers):
        return response.view("Too many attempts, please try again tomorrow", 429)


class TestLimitingRequest(TestCase):
    def setUp(self):
        super().setUp()
        # register limiters
        RateLimiter.register("test_global", GlobalLimiter("4/minute"))
        RateLimiter.register("test_guests", GuestsOnlyLimiter("2/minute"))
        RateLimiter.register("test_custom", CustomLimit())
        self.addRoutes(
            Route.get("/throttled/global", "WelcomeController@show").middleware(
                "throttle:test_global"
            ),
            Route.get("/throttled/guests", "WelcomeController@show").middleware(
                "throttle:test_guests"
            ),
            Route.get("/throttled/arg", "WelcomeController@show").middleware(
                "throttle:2/hour"
            ),
            Route.get("/throttled/custom", "WelcomeController@show").middleware(
                "throttle:test_custom"
            ),
        )

    def tearDown(self):
        super().tearDown()
        # delete cache entries between tests for idempotent tests
        self.application.make("cache").store().flush()
        # always restore time if it has been faked
        self.restoreTime()

    def test_limit_from_middleware_arg(self):
        self.get("/throttled/arg").assertOk()
        self.get("/throttled/arg").assertOk()
        with self.assertRaises(ThrottleRequestsException):
            self.get("/throttled/arg")
        # set time 2 hours later
        self.fakeTimeInFuture(2, "hours")
        self.get("/throttled/arg").assertOk()

    def test_limiter_in_production(self):
        self.withExceptionsHandling()
        with self.debugMode(False):
            count = 0
            for _ in range(4):
                count += 1
                (
                    self.get("/throttled/global")
                    .assertOk()
                    .assertHasHeader("X-RateLimit-Limit", "4")
                    .assertHasHeader("X-RateLimit-Remaining", str(4 - count))
                )

            (
                self.get("/throttled/global")
                .assertLimited()
                .assertHasHeader("Retry-After")
                .assertHasHeader("X-RateLimit-Reset")
                .assertHasHeader("X-RateLimit-Limit", "4")
                .assertHasHeader("X-RateLimit-Remaining", "0")
            )

    def test_limit_guests_users_only(self):
        # can make only 2 requests in one minute
        self.get("/throttled/guests").assertOk().assertHasHeader(
            "X-RateLimit-Limit", "2"
        )
        self.get("/throttled/guests").assertOk()
        with self.assertRaises(ThrottleRequestsException):
            self.get("/throttled/guests")
        # no limits if authenticated, wait for PR#551 to be merged which fix actingAs
        # self.actingAs(User.first()).get(
        #     "/throttled/guests"
        # ).assertOk().assertHeaderMissing("X-RateLimit-Limit")

    def test_using_custom_response(self):
        self.get("/throttled/custom").assertOk()
        self.get("/throttled/custom").assertOk()
        self.get("/throttled/custom").assertLimited().assertContains(
            "Too many attempts, please try again tomorrow"
        )
