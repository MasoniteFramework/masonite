''' A Module Description '''
from app.http.providers.view import view

class WelcomeController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    @staticmethod
    def show():
        ''' Show Welcome Template '''
        return view('welcome')
