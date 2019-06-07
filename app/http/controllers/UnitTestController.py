"""A UnitTestController Module."""

from masonite.request import Request
from masonite.controllers import Controller


class UnitTestController(Controller):
    """UnitTestController Controller Class."""
    
    def __init__(self, request: Request):
        """UnitTestController Initializer
        
        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self):
        return 'got'

    def store(self):
        return 'posted'

    def params(self):
        return self.request.input('test')

    def get_params(self):
        return self.request.input('test')

    def user(self):
        return self.request.user().name

    def json(self):
        return self.request.input('test')

    def patch(self):
        return self.request.input('test')
