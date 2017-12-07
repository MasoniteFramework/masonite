''' A Module Description '''
from app.http.providers.view import view

class LoginController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    @staticmethod
    def show():
        return view('login')
