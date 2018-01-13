''' Class for the authentication middleware '''
from masonite.facades.Auth import Auth

class RouteMiddleware(object):
    ''' Middleware class which loads the current user into the request '''

    def __init__(self):
        print('router middleware initialized')

    def before(self, request):
        ''' Register as a before middleware to be ran before the request '''
        if not request.user():
            request.redirect('/login')

        print('before route middleware')

    def after(self, request):
        pass
