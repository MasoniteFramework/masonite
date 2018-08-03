""" Load User Middleware"""
from masonite.facades.Auth import Auth

class LoadUserMiddleware:
    """Middleware class which loads the current user into the request
    """

    def __init__(self, Request):
        """Inject Any Dependencies From The Service Container
        
        Arguments:
            Request {masonite.request.Request} -- The Masonite request object.
        """

        self.request = Request

    def before(self):
        """Run This Middleware Before The Route Executes
        """

        self.load_user(self.request)
        return self.request

    def after(self):
        """Run This Middleware After The Route Executes
        """

        pass

    def load_user(self, request):
        """Load user into the request
        
        Arguments:
            request {masonite.request.Request} -- The Masonite request object.
        """
        
        request.set_user(Auth(request).user())
