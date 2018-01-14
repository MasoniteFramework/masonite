''' Class for the authentication middleware '''
from masonite.facades.Auth import Auth

class LoadUserMiddleware(object):
    ''' Middleware class which loads the current user into the request '''

    def __init__(self, request):
        self.request = request

    def before(self):
        ''' Register as a before middleware to be ran before the request '''
        self.load_user(self.request)
        return self.request

    def after(self):
        ''' Register as an after middleware to be ran after the request '''
        pass

    def load_user(self, request):
        ''' Load user into the request '''
        request.set_user(Auth(request).user())
