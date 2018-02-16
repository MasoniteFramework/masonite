''' Welcome The User To Masonite '''

from masonite.request import Request

class WelcomeController(object):
    ''' Controller For Welcoming The User '''

    def show(self, Application, request: Request):
        ''' Show Welcome Template '''
        return view('welcome', {'app': Application})
