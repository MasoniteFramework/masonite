''' A Module Description '''
from masonite.facades.Auth import Auth

class HomeController(object):
    ''' Home Dashboard Controller '''

    def __init__(self):
        pass

    def show(self, Request, Application):
        if not Auth(Request).user():
            Request.redirect('/login')
        return view('auth/home', {'app': Application, 'Auth': Auth(Request)})
