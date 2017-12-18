''' A Module Description '''
from app.http.providers.view import view
from config import application
from packages.facades.Auth import Auth

class WelcomeController(object):
    ''' Controller for welcoming the user '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Show Welcome Template '''
        return view('welcome', {'app': application})
