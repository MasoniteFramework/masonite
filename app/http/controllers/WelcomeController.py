''' A Module Description '''
from app.http.providers.view import view
from config import app

class WelcomeController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Show Welcome Template '''
        return view('welcome', {'app': app})
