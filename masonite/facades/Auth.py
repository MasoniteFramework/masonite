''' Authentication Class '''
import uuid

from config import auth

class Auth(object):
    ''' This class will be used to authenticate users based on the config/auth.py file '''

    def __init__(self, request):
        self.request = request

    def user(self):
        ''' Returns the model specified in the auth.py configuration '''
        try:
            if self.request.get_cookie('token'):
                return auth.AUTH['model'].get(
                    auth.AUTH['model'].token == self.request.get_cookie('token')
                )
            
            return False
        except Exception as exception:
            pass

        return False

    def login(self, name, password):
        ''' Login the user based on the parameters provided '''
        auth_column = getattr(auth.AUTH['model'], auth.AUTH['model']._meta.auth_column)
        try:
            model = auth.AUTH['model'].get(
                auth_column == name,
            )
            if model.password.check_password(password):
                token = uuid.uuid4()
                model.token = token
                model.save()
                self.request.cookie('token', token)
                return model
        except Exception as exception:
            raise exception

        return False

    def logout(self):
        self.request.cookie('token', '; expires=Thu, 01 Jan 1970 00:00:00 GMT')
        return self
