"""A LoginController Module."""

from masonite.auth import Auth
from masonite.request import Request
from masonite.view import View


class LoginController:
    """Login Form Controller."""

    def __init__(self):
        """LoginController Constructor."""
        pass

    def show(self, request: Request, view: View):
        """Show the login page.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            view {masonite.view.View} -- The Masonite view class.

        Returns:
            masonite.view.View -- Returns the Masonite view class.
        """
        if request.user():
            return request.redirect('/home')
        return view.render('auth/login', {'app': request.app().make('Application'), 'Auth': Auth(request)})

    def store(self, request: Request):
        """Login the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        if Auth(request).login(request.input('email'), request.input('password')):
            return request.redirect('/home')

        return request.redirect('/login')

    def logout(self, request: Request):
        """Log out the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        Auth(request).logout()
        return request.redirect('/login')
