"""The ConfirmController Module."""
import datetime

from masonite.auth import Auth
from masonite.auth.Sign import Sign
from masonite.request import Request
from masonite.view import View
from masonite.auth import MustVerifyEmail
from app.User import User


class ConfirmController:
    """The ConfirmController class."""

    def __init__(self):
        """The ConfirmController Constructor."""
        pass

    def verify_show(self, request: Request, view: View, auth: Auth):
        """Show the Verify Email page for unverified users.

        Arguments:
            request {masonite.request.request} -- The Masonite request class.
            request {masonite.view.view} -- The Masonite view class.
            request {masonite.auth.auth} -- The Masonite Auth class.

        Returns:
            [type] -- [description]
        """
        return view.render('auth/verify', {'app': request.app().make('Application'), 'Auth': auth})

    def confirm_email(self, request: Request, view: View, auth: Auth):
        """Confirm User email and show the correct response.

        Arguments:
            request {masonite.request.request} -- The Masonite request class.
            request {masonite.view.view} -- The Masonite view class.
            request {masonite.auth.auth} -- The Masonite Auth class.

        Returns:
            [type] -- [description]
        """
        sign = Sign()
        token = sign.unsign(request.param('id'))

        if token is not None:
            tokenParts = token.split("::")
            if len(tokenParts) > 1:
                user = self.get_user.find(1)

                if user.verified_at is None:
                    timestamp = datetime.datetime.fromtimestamp(float(tokenParts[1]))
                    now = datetime.datetime.now()
                    timestamp_plus_10 = timestamp + datetime.timedelta(minutes=10)

                    if now < timestamp_plus_10:
                        user.verified_at = datetime.datetime.now()
                        user.save()

                        return view.render('auth/confirm', {'app': request.app().make('Application'), 'Auth': auth})

        return view.render('auth/error', {'app': request.app().make('Application'), 'Auth': auth})

    def get_user(self, user_id):
        """Get the user from the database.

        Arguments:
            user_id {str} -- The users id

        Returns:
            [User] -- [User model]
        """
        return User.find(user_id)

    def send_verify_email(self, request: Request):
        user = request.user()

        if isinstance(user, MustVerifyEmail):
            request.app().resolve(user.verify_email)

        return request.redirect('/home')
