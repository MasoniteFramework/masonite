
from masonite.helpers import config
from masonite.request import Request
from masonite.drivers import BaseDriver
from masonite.exceptions import DriverLibraryNotFound
import pendulum
from masonite.helpers import cookie_expire_time
from masonite.auth import Auth


class AuthJwtDriver(BaseDriver):

    def __init__(self, request: Request):
        self.request = request
        try:
            import jwt
            self.jwt = jwt
        except ImportError:
            raise DriverLibraryNotFound("Please install pyjwt by running 'pip install pyjwt'")

    def user(self, auth_model):
        if self.request.get_cookie('token'):
            token = self.jwt.decode(self.request.get_cookie('token'), 'secret', algorithms=['HS256'])
            expired = token['expired']
            token.pop('expired')
            if not pendulum.parse(expired).is_past():
                return auth_model.hydrate(token)
            else:
                if config('auth.drivers.jwt.reauthentication', True):
                    auth_model = Auth(self.request).login_by_id(token[auth_model.__primary_key__])
                else:
                    auth_model.hydrate(token)

                token.update({
                    'expired': cookie_expire_time('5 minutes')
                })
                self.request.cookie('token', token)
                return auth_model
        return False

    def save(self, _, **kwargs):
        from config.application import KEY
        model = kwargs.get('model', False)
        serialized_dictionary = model.serialize()
        serialized_dictionary.update({
            'expired': cookie_expire_time('5 minutes')
        })
        token = self.jwt.encode(serialized_dictionary, KEY, algorithm='HS256')
        token = bytes(token).decode('utf-8')
        self.request.cookie('token', token)


    def delete(self):
        self.request.delete_cookie('token')
