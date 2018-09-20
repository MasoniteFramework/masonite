""" The RegisterController Module """

from config import auth
from masonite.auth import Auth
from masonite.helpers import password as bcrypt_password
from masonite.request import Request
from masonite.view import View


class RegisterController:
    """The RegisterController class.
    """

    def __init__(self):
        """The RegisterController Constructor
        """

        pass

    def show(self, request: Request, view: View):
        """Show the registration page.

        Arguments:
            Request {masonite.request.request} -- The Masonite request class.

        Returns:
            [type] -- [description]
        """

        return view.render('auth/register', {'app': request.app().make('Application'), 'Auth': Auth(request)})

    def store(self, request: Request):
        """Register the user with the database.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """

        password = bcrypt_password(request.input('password'))

        auth.AUTH['model'].create(
            name=request.input('name'),
            password=password,
            email=request.input('email'),
        )

        # Login the user
        if Auth(request).login(request.input(auth.AUTH['model'].__auth__), request.input('password')):
            # Redirect to the homepage
            return request.redirect('/home')

        # Login failed. Redirect to the register page.
        return request.redirect('/register')
