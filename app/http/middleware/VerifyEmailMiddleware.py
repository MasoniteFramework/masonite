''' Verify Email Middleware '''
from masonite.request import Request

class VerifyEmailMiddleware:
    ''' Verify Email Middleware '''

    def __init__(self, request: Request):
        self.request = request

    def before(self):
        pass

    def after(self):
        user = self.request.user()

        if user and user.verified_at is None:
            self.request.redirect('/email/verify')
