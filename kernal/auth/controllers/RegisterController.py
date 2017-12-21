''' A Module Description '''
from masonite.view import view
from masonite.facades.Auth import Auth
from config import application
from config import auth

class RegisterController(object):
    ''' Class Docstring Description '''

    def __init__(self):
        pass

    def show(self, request):
        ''' Show the registration page '''
        return view('auth/register', {'app': application, 'Auth': Auth(request)})

    def store(self, request):
        ''' Register a new user '''

        # register the user
        auth.AUTH['model'].create(
            name=request.input('name'),
            password=request.input('password'),
            email=request.input('email'),
        )

        # login the user
        # redirect to the homepage
        if Auth(request).login(request.input('name'), request.input('password')):
            return request.redirect('/home')

        return request.redirect('/register')
