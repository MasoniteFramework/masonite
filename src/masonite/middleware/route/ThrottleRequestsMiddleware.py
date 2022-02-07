from ..middleware import Middleware


class ThrottleRequestsMiddleware(Middleware):
    def before(self, request, response, limits):
        import pdb

        pdb.set_trace()
        return request

    def after(self, request, response, limits):
        import pdb

        pdb.set_trace()
        return request
