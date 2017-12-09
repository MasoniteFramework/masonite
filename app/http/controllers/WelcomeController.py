''' A Module Description '''
from app.http.providers.view import view
from config import app

class WelcomeController(object):
    ''' Controller for welcoming the user '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Show Welcome Template '''
        return view('welcome', {'app': app})
