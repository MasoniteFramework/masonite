import hashlib

from ..middleware import Middleware
from ...facades import RateLimiter
from ...rates import UnlimitedRate
from ...rates.Limit import Limit
from ...exceptions import ThrottleRequestsException


class ThrottleRequestsMiddleware(Middleware):
    def before(self, request, response, limit):

        rate = self.get_limit(request, limit)
        if isinstance(rate, UnlimitedRate):
            return request
        else:
            key = hashlib.md5(str(limit + rate.key).encode()).hexdigest()
            if RateLimiter.too_many_attempts(key, rate.max_attempts):
                headers = self.get_headers(key, rate.max_attempts, True)
                raise ThrottleRequestsException(headers=headers)
            else:
                # delay rates are in minutes
                RateLimiter.hit(key, rate.delay * 60)

        # add headers to response
        response.with_headers(self.get_headers(key, rate.max_attempts))

        return request

    def after(self, request, response, limits):
        return request

    def get_limit(self, request, limit):
        if "/" in limit:
            return Limit.from_str(limit)
        else:
            limiter = RateLimiter.get_limiter(limit)
            return limiter.allow(request)

    def get_headers(self, key, max_attempts, limited=False):
        headers = {
            "X-RateLimit-Limit": max_attempts,
            "X-RateLimit-Remaining": RateLimiter.remaining(key, max_attempts),
        }
        if limited:
            headers.update(
                {
                    "Retry-After": RateLimiter.available_in(key),
                    "X-RateLimit-Reset": RateLimiter.available_at(key),
                }
            )
        return headers
