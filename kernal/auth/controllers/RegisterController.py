''' A Module Description '''
from app.http.providers.view import view

class RegisterController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Show the registration page '''
        return view('auth/register')
