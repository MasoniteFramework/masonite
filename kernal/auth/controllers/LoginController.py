''' A Module Description '''
from app.http.providers.view import view

class LoginController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Return the login page '''
        return view('auth/login')
