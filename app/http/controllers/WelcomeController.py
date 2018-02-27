''' Welcome The User To Masonite '''

class WelcomeController(object):
    ''' Controller For Welcoming The User '''

    def show(self, Application):
        ''' Show Welcome Template '''
        return view('welcome', {'app': Application})
