from masonite.middleware import Middleware


class __class__(Middleware):
    def before(self, request, response):
        return request

    def after(self, request, response):
        return request
