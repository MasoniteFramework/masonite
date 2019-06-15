"""The HomeController Module."""

from masonite.auth import Auth
from masonite.request import Request
from masonite.view import View


class HomeController:
    """Home Dashboard Controller."""

    def __init__(self):
        pass

    def show(self, request: Request, view: View, auth: Auth):
        if not auth.user():
            request.redirect('/login')
        return view.render('auth/home')
