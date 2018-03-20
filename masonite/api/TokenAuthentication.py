from masonite.exceptions import ApiNotAuthenticated, NoApiTokenFound
from urllib.parse import parse_qs

# TODO:
#     - load a model in to retrieve it's access token if it's not the current model that has it
class TokenAuthentication:

    authentication_model = None

    def authenticate(self):
        if not self.authentication_model:
            self.authentication_model = self.obj
        
        if not self.request.has('token'):
            raise NoApiTokenFound

        if not self.authentication_model.where('token', self.request.input('token')).count():
            raise ApiNotAuthenticated
        
        # Delete the token input
        if self.request.is_not_get_request():
            build_new_inputs = {}
            for i in self.request.params:
                build_new_inputs[i] = self.request.params[i]
            
            build_new_inputs.pop('token')
            self.request.params = build_new_inputs
    
        
    def tokens_from_model(self, model):
        self.authentication_model = model
        return self
