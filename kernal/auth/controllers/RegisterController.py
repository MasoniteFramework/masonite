''' A Module Description '''
from app.http.providers.view import view

class RegisterController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    @staticmethod
    def show():
        return view('register')
