import hashlib
from typing import TYPE_CHECKING

from attr import has

if TYPE_CHECKING:
    from ...request import Request
    from ...response import Response

from ..middleware import Middleware
from ...facades import RateLimiter
from ...rates.Limit import Limit
from ...exceptions import ThrottleRequestsException


class ThrottleRequestsMiddleware(Middleware):
    def before(
        self, request: "Request", response: "Response", limit_string: str
    ) -> "Request":
        response_callback = None
        if "/" in limit_string:
            limit = Limit.from_str(limit_string)
        else:
            limiter = RateLimiter.get_limiter(limit_string)
            if hasattr(limiter, "get_response"):
                response_callback = limiter.get_response
            limit = limiter.allow(request)

        if limit.is_unlimited():
            return request
        else:
            key = hashlib.md5(str(limit_string + limit.key).encode()).hexdigest()
            if RateLimiter.too_many_attempts(key, limit.max_attempts):
                headers = self.get_headers(key, limit.max_attempts, True)
                # raise exception or show custom response of limiter
                if response_callback:
                    return response_callback(request, response, headers)
                else:
                    raise ThrottleRequestsException(headers=headers)
            else:
                # delay rates are in minutes
                RateLimiter.hit(key, limit.delay * 60)

        # add headers to response
        response.with_headers(self.get_headers(key, limit.max_attempts))

        return request

    def after(
        self, request: "Request", response: "Response", limit_string: str
    ) -> "Request":
        return request

    def get_headers(self, key: str, max_attempts: int, limited: bool = False) -> dict:
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
