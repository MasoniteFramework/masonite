""" The ConfirmController Module """
import time, datetime

from masonite.auth import Auth
from masonite.auth.Sign import Sign
from masonite.request import Request
from masonite.view import View
from masonite.auth.MustVerifyEmail import MustVerifyEmail
from app.User import User


class ConfirmController:
    """The ConfirmController class.
    """

    def __init__(self):
        """The RegisterController Constructor
        """
        pass

    def verify_show(self, request: Request, view: View):
        return view.render('auth/verify', {'app': request.app().make('Application'), 'Auth': Auth(request)})

    def confirm_email(self, request: Request, view: View):
        sign = Sign()
        token = sign.unsign(request.param('id'))

        if token is not None:
            tokenParts = token.split("::")
            if len(tokenParts) > 1:
                id = tokenParts[0]
                user = User.find(id)
                
                if user.verified_at is None:
                    timestamp = datetime.datetime.fromtimestamp(float(tokenParts[1]))
                    now = datetime.datetime.now()
                    timestamp_plus_10 = timestamp + datetime.timedelta(minutes = 10)
                
                    if now < timestamp_plus_10:
                        user.verified_at = datetime.datetime.now()
                        user.save()

                        return view.render('auth/confirm', {'app': request.app().make('Application'), 'Auth': Auth(request)})


        return view.render('auth/error', {'app': request.app().make('Application'), 'Auth': Auth(request)})