"""Welcome The User To Masonite."""

from src.masonite.view import View
from src.masonite.controllers import Controller


class WelcomeController(Controller):
    """Controller For Welcoming The User."""

    def show(self, view: View):
        """Show the welcome page.

        Arguments:
            view {masonite.view.View} -- The Masonite view class.
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.view.View -- The Masonite view class.
        """
        return view.render('welcome')
