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

    def reset(self, request: Request, auth: Auth):
        token = request.param('token')
        user = AUTH['model'].where('remember_token', token).first()
        if user:
            return view('auth/reset', {'token': token, 'app': config('application'), 'Auth': auth})

    def send(self, request: Request, session: Session, mail: Mail, validate: Validator):
        errors = request.validate(
            validate.required(['email']),
            validate.email('email')
        )

        if errors:
            request.session.flash('errors', {
                'email': errors.get('email', None),
            })
            return request.back()

        email = request.input('email')
        user = AUTH['model'].where('email', email).first()

        if user:
            if not user.remember_token:
                user.remember_token = str(uuid.uuid4())
                user.save()
            message = 'Please visit {}/password/{}/reset to reset your password'.format(env('SITE', 'http://localhost:8000'), user.remember_token)
            mail.subject('Reset Password Instructions').to(email).send(message)
            session.flash('success', 'Email sent. Follow the instruction in the email to reset your password.')
            return request.redirect('/password')
        else:
            session.flash('error', 'Could not send reset email. Please enter correct email.')
            return request.redirect('/password')

    def update(self, request: Request, validate: Validator):
        errors = request.validate(
            validate.required(['password']),
            # TODO: only available in masonite latest versions (which are not compatible with Masonite 2.2)
            # validate.strong('password', length=8, special=1, uppercase=1)
        )

        if errors:
            request.session.flash('errors', {
                'password': errors.get('password', None)
            })
            return request.back()

        user = AUTH['model'].where('remember_token', request.param('token')).first()
        if user:
            user.password = bcrypt_password(request.input('password'))
            user.save()
            return request.redirect('/login')
