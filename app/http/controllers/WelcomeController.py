''' A Module Description '''
from masonite.view import view
from masonite.request import Request

class WelcomeController(object):
    ''' Controller for welcoming the user '''

    def __init__(self):
        pass

    def show(self, Application, request: Request):
        ''' Show Welcome Template '''
        return view('welcome', {'app': Application})
