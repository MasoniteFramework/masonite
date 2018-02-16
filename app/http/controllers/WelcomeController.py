''' A Module Description '''

from masonite.request import Request

class WelcomeController(object):
    ''' Controller for welcoming the user '''

    def show(self, Application, request: Request):
        ''' Show Welcome Template '''
        return view('welcome', {'app': Application})
