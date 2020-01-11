"""A PasswordController Module."""

import uuid

from masonite import env, Mail, Session
from masonite.auth import Auth
from masonite.helpers import config, password as bcrypt_password
from masonite.request import Request
from masonite.view import View
from masonite.validation import Validator
from config.auth import AUTH


class PasswordController:
    """Password Controller."""

    def forget(self, view: View, auth: Auth):
        return view.render('auth/forget', {'app': config('application'), 'Auth': auth})

    def reset(self, view: View, request: Request, auth: Auth):
        token = request.param('token')
        user = AUTH['guards']['web']['model'].where('remember_token', token).first()
        if user:
            return view.render('auth/reset', {'token': token, 'app': config('application'), 'Auth': auth})

    def send(self, request: Request, session: Session, mail: Mail, validate: Validator):
        errors = request.validate(
            validate.required('email'),
            validate.email('email')
        )

        if errors:
            return request.back().with_errors(errors)

        email = request.input('email')
        user = AUTH['guards']['web']['model'].where('email', email).first()

        if user:
            if not user.remember_token:
                user.remember_token = str(uuid.uuid4())
                user.save()
            message = 'Please visit {}/password/{}/reset to reset your password'.format(env('SITE', 'http://localhost:8000'), user.remember_token)
            mail.subject('Reset Password Instructions').to(user.email).send(message)

        session.flash('success', 'If we found that email in our system then the email has been sent. Please follow the instructions in the email to reset your password.')
        return request.redirect('/password')

    def update(self, request: Request, validate: Validator):
        errors = request.validate(
            validate.required('password'),
            # TODO: only available in masonite latest versions (which are not compatible with Masonite 2.2)
            validate.strong(
                'password',
                length=8, special=1, uppercase=1,
                # breach=True checks if the password has been breached before.
                # Requires 'pip install pwnedapi'
                breach=False
            )
        )

        if errors:
            return request.back().with_errors(errors)

        user = AUTH['guards']['web']['model'].where(
            'remember_token', request.param('token')).first()
        if user:
            user.password = bcrypt_password(request.input('password'))
            user.save()
            return request.redirect('/login')
