''' Verify Email Middleware '''
from masonite.exceptions import InvalidCSRFToken
from masonite.request import Request
from masonite.view import View
from jinja2 import Markup


class VerifyEmailMiddleware:
    ''' Verify Email Middleware '''

    def __init__(self, request: Request, csrf: Csrf, view: View):
        self.request = request
        self.view = view

    def before(self):
        user = self.request.user()
        if(user.verified_at is None){
            self.request.redirect('/email/verify')
        }

    def after(self):
        pass
