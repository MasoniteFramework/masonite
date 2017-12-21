''' A Module Description '''
from masonite.view import view
from masonite.facades.Auth import Auth
from config import application


class LoginController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Return the login page '''
        return view('auth/login', {'app': application, 'Auth': Auth(request)})

    def store(self, request):
        if Auth(request).login(request.input('username'), request.input('password')):
            request.redirect('/home')
        else:
            request.redirect('/login')
        return 'check terminal'

    def logout(self, request):
        Auth(request).logout()
        return request.redirect('/login')
