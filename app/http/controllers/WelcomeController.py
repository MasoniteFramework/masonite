"""Welcome The User To Masonite."""

from masonite.controllers import Controller
from masonite.request import Request
from masonite.view import View


class WelcomeController(Controller):
    """Controller For Welcoming The User."""

    def show(self, view: View, request: Request):
        """Show the welcome page.

        Arguments:
            view {masonite.view.View} -- The Masonite view class.
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.view.View -- The Masonite view class.

        """
        return view.render("welcome")
