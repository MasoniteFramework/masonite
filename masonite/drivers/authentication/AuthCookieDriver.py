
from masonite.helpers import config
from masonite.request import Request
from masonite.drivers import BaseDriver


class AuthCookieDriver(BaseDriver):

    def __init__(self, request: Request):
        self.request = request

    def user(self, auth_model):
        if self.request.get_cookie('token') and auth_model:
            return auth_model.where(
                'remember_token', self.request.get_cookie('token')
            ).first()
        
        return False

    def save(self, remember_token, **kwargs):
        return self.request.cookie('token', remember_token)

    def delete(self):
        return self.request.delete_cookie('token')
