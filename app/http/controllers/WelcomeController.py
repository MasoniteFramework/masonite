""" Welcome The User To Masonite """
from masonite.view import View

class WelcomeController:
    """Controller For Welcoming The User
    """

    def show(self, view: View, Application):
        """Show Welcome Template 
        """

        return view.render('welcome', {'app': Application})
