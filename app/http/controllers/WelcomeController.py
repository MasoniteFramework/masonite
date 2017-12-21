''' A Module Description '''
from masonite.view import view
from config import application

class WelcomeController(object):
    ''' Controller for welcoming the user '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Show Welcome Template '''
        return view('welcome', {'app': application})
