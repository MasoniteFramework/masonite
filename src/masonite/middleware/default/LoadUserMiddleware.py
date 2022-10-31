from .. import Middleware
from ...facades import Auth


class LoadUserMiddleware(Middleware):
    def before(self, request, _):
        request.set_user(Auth.user())
        return request

    def after(self, request, _):
        return request
