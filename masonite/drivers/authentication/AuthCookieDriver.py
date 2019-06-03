
from masonite.contracts import AuthContract
from masonite.drivers import BaseDriver
from masonite.request import Request


class AuthCookieDriver(BaseDriver, AuthContract):

    def __init__(self, request: Request):
        self.request = request

    def user(self, auth_model):
        if self.request.get_cookie('token') and auth_model:
            return auth_model.where(
                'remember_token', self.request.get_cookie('token')
            ).first()

        return False

    def save(self, remember_token, **_):
        return self.request.cookie('token', remember_token)

    def delete(self):
        return self.request.delete_cookie('token')
