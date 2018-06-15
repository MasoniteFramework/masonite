""" Authentication Class """
import bcrypt
import uuid


class Auth:
    """
    This class will be used to authenticate users based on the config/auth.py file
    """
    
    _once = False

    def __init__(self, request, auth_model=None):
        self.request = request

        if auth_model:
            self.auth_model = auth_model
        else:
            from config import auth
            self.auth_model = auth.AUTH['model']

    def user(self):
        """
        Returns the model specified in the auth.py configuration
        """
        try:
            if self.request.get_cookie('token'):
                return self.auth_model.where(
                    'remember_token', self.request.get_cookie('token')
                ).first()

            return False
        except Exception as exception:
            raise exception

        return None

    def login(self, name, password):
        """
        Login the user based on the parameters provided
        """ 
        auth_column = self.auth_model.__auth__
        try:
            model = self.auth_model.where(auth_column, name).first()

            if model and bcrypt.checkpw(bytes(password, 'utf-8'), bytes(model.password, 'utf-8')):
                if not self._once:
                    remember_token = str(uuid.uuid4())
                    model.remember_token = remember_token
                    model.save()
                    self.request.cookie('token', remember_token)
                return model

        except Exception as exception:
            raise exception

        return False

    def logout(self):
        self.request.delete_cookie('token')
        return self
    
    def login_by_id(self, id):
        model = self.auth_model.find(id)

        if model:
            if not self._once:
                remember_token = str(uuid.uuid4())
                model.remember_token = remember_token
                model.save()
                self.request.cookie('token', remember_token)
            return model
        
        return False
    
    def once(self):
        self._once = True
        return self
