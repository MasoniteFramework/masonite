''' A Module Description '''
from masonite.facades.Auth import Auth


class LoginController(object):
    ''' Login Form Controller '''

    def __init__(self):
        pass

    def show(self, Request, Application):
        ''' Show the login page '''
        return view('auth/login', {'app': Application, 'Auth': Auth(Request)})

    def store(self, Request):
        if Auth(Request).login(Request.input('username'), Request.input('password')):
            Request.redirect('/home')
        else:
            Request.redirect('/login')
        return 'check terminal'

    def logout(self, Request):
        Auth(Request).logout()
        return Request.redirect('/login')
