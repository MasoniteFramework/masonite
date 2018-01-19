''' Authentication Class '''
import uuid

from config import auth
import bcrypt

class Auth(object):
    ''' This class will be used to authenticate users based on the config/auth.py file '''

    def __init__(self, request):
        self.request = request

    def user(self):
        ''' Returns the model specified in the auth.py configuration '''
        try:
            if self.request.get_cookie('token'):
                return auth.AUTH['model'].where(
                    'remember_token', self.request.get_cookie('token')
                ).first()
            
            return False
        except Exception as exception:
            raise exception

        return None

    def login(self, name, password):
        ''' Login the user based on the parameters provided '''
        auth_column = auth.AUTH['model'].__auth__
        try:
            model = auth.AUTH['model'].where(auth_column, name).first()

            if model and bcrypt.checkpw(bytes(password, 'utf-8'), bytes(model.password, 'utf-8')):
                remember_token = str(uuid.uuid4())
                model.remember_token = remember_token
                model.save()
                self.request.cookie('token', remember_token)
                return model

        except Exception as exception:
            raise exception

        return False

    def logout(self):
        self.request.cookie('token', '; expires=Thu, 01 Jan 1970 00:00:00 GMT')
        return self
