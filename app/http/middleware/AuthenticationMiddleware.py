''' Authentication Middleware '''

class AuthenticationMiddleware:
    ''' Middleware To Check If The User Is Logged In '''

    def __init__(self, Request):
        ''' Inject Any Dependencies From The Service Container '''
        self.request = Request

    def before(self):
        ''' Run This Middleware Before The Route Executes '''
        if not self.request.user():
            self.request.redirect_to('login')

    def after(self):
        ''' Run This Middleware After The Route Executes '''
        pass
