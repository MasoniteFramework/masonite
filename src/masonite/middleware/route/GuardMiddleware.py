from ...facades import Auth
from .. import Middleware


class GuardMiddleware(Middleware):
    def before(self, request, _, guard):
        Auth.guard(guard)
        return request

    def after(self, request, _, __):
        return request
