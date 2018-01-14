''' Class for the authentication middleware '''

class AuthenticationMiddleware(object):
    ''' Middleware class which loads the current user into the request '''

    def __init__(self, request):
        self.request = request

    def before(self):
        ''' Register as a before middleware to be ran before the request '''
        if not self.request.user():
            self.request.redirectTo('login')

    def after(self):
        pass
