"""A LoginController Module."""

from masonite.auth import Auth
from masonite.request import Request
from masonite.view import View
from masonite.helpers import config
from masonite.validation import Validator


class LoginController:
    """Login Form Controller."""

    def __init__(self):
        """LoginController Constructor."""
        pass

    def show(self, request: Request, view: View, auth: Auth):
        """Show the login page.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            view {masonite.view.View} -- The Masonite view class.
            auth {masonite.auth.auth} -- The Masonite auth class.

        Returns:
            masonite.view.View -- Returns the Masonite view class.
        """
        if request.user():
            return request.redirect('/home')
        return view.render('auth/login', {'app': config('application'), 'Auth': auth})

    def store(self, request: Request, auth: Auth, validate: Validator):
        """Login the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            auth {masonite.auth.auth} -- The Masonite auth class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        errors = request.validate(
            validate.required(['email', 'password']),
            validate.email('email'),
            # TODO: only available in masonite latest versions (which are not compatible with Masonite 2.2)
            # validate.strong('password', length=8, special=1, uppercase=1)
        )

        if errors:
            request.session.flash('errors', {
                'email': errors.get('email', None),
                'password': errors.get('password', None)
            })
            return request.back()

        if auth.login(request.input('email'), request.input('password')):
            return request.redirect('/home')

        return request.redirect('/login')

    def logout(self, request: Request, auth: Auth):
        """Log out the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            auth {masonite.auth.auth} -- The Masonite auth class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        auth.logout()
        return request.redirect('/login')
