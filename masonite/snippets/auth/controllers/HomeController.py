"""The HomeController Module."""

from masonite.auth import Auth
from masonite.request import Request
from masonite.view import View


class HomeController:
    """Home Dashboard Controller."""

    def __init__(self):
        pass

    def show(self, request: Request, view: View):
        if not Auth(request).user():
            request.redirect('/login')
        return view.render('auth/home', {'app': request.app().make('Application'), 'Auth': Auth(request)})
