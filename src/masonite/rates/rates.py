from .Limit import Limit


class Rate:
    def __init__(self):
        pass

    def allow(self, request):
        # return Limit.unlimited()
        # return Limit.per_minute(500)
        # return Limit.per_hour(500)
        # return Limit.per_day(500)
        # return Limit.per("60/min")
        # return Limit.custom(500, 60)
        if request.user():
            return Limit.per_minute(100).by(request.user().get_id())
        else:
            # default of by is to use request.ip
            return Limit.per_day(100).by(request.ip())

    def response(self):
        return Response.view("Too many attempts", 429)


class GlobalRate(Rate):
    """Apply a global limit"""

    def __init__(self, limit):
        self.limit = limit

    def allow(self, request):
        return Limit.from_str(self.limit)


class UnlimitedRate(Rate):
    def allow(self, request):
        return Limit.unlimited()


class LimitedForGuestsRate(Rate):
    """Apply a limit for guests only."""

    def __init__(self, limit):
        self.limit = limit

    def allow(self, request):
        if request.user():
            return Limit.unlimited()
        else:
            return Limit.from_str(self.limit).by("127.0.0.1")


# class CustomLimit:
#     def allow(self, request):
#         if request.user():
#             return Limit.per_minute(100).by(request.user().get_id())
#         else:
#             # default of by is to use request.ip
#             return Limit.per_day(100).by(request.ip())

#     def response(self, request):
#         return "Too many attempts"
