"""The RegisterController Module."""

from config import auth
from masonite.auth import Auth
from masonite.helpers import password as bcrypt_password
from masonite.request import Request
from masonite.view import View
from masonite.auth import MustVerifyEmail
from masonite.managers import MailManager


class RegisterController:
    """The RegisterController class."""

    def __init__(self):
        """The RegisterController Constructor."""
        pass

    def show(self, request: Request, view: View):
        """Show the registration page.

        Arguments:
            Request {masonite.request.request} -- The Masonite request class.

        Returns:
            masonite.view.View -- The Masonite View class.
        """
        return view.render('auth/register', {'app': request.app().make('Application'), 'Auth': Auth(request)})

    def store(self, request: Request, mail_manager: MailManager):
        """Register the user with the database.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        user = auth.AUTH['model'].create(
            name=request.input('name'),
            password=bcrypt_password(request.input('password')),
            email=request.input('email'),
        )

        if isinstance(user, MustVerifyEmail):
            user.verify_email(mail_manager, request)

        # Login the user
        if Auth(request).login(request.input(auth.AUTH['model'].__auth__), request.input('password')):
            # Redirect to the homepage
            return request.redirect('/home')

        # Login failed. Redirect to the register page.
        return request.redirect('/register')
