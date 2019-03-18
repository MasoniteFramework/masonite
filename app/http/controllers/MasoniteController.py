"""A MasoniteController Module."""

from masonite.request import Request
from masonite.view import View

class MasoniteController:
    """MasoniteController Controller Class."""
    
    def __init__(self, request: Request):
        """MasoniteController Initializer
        
        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        pass