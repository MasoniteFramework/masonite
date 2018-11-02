''' Load User Middleware'''

from masonite.request import Request


class AddAttributeMiddleware:
    ''' Middleware class which loads the current user into the request '''

    def __init__(self, request: Request):
        ''' Inject Any Dependencies From The Service Container '''
        self.request = Request

    def before(self):
        ''' Run This Middleware Before The Route Executes '''
        self.request.attribute = True

    def after(self):
        ''' Run This Middleware After The Route Executes '''
        pass
