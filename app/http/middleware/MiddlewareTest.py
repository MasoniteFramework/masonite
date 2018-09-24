''' Load User Middleware'''

from masonite.request import Request


class MiddlewareTest:
    ''' Middleware class which loads the current user into the request '''

    def __init__(self, request: Request):
        ''' Inject Any Dependencies From The Service Container '''
        self.request = request

    def before(self):
        ''' Run This Middleware Before The Route Executes '''
        self.request.path = 'test/middleware/before/ran'

    def after(self):
        ''' Run This Middleware After The Route Executes '''
        pass
