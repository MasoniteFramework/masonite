import json
from masonite.exceptions import ApiNotAuthenticated, NoApiTokenFound

# TODO: 
#    - create tokens
#        - need to make a helper class which will create tokens
class Resource:

    exclude = []
    url = None

    def __init__(self, obj):
        self.obj = obj
        self.obj.__hidden__ = self.exclude
        if not self.url:
            self.url = '/api/{0}'.format(obj().__class__.__name__.lower())
        

    def handle(self):

        # Run authentication if one exists
        if hasattr(self, 'authenticate'):
            try:
                self.authenticate()
            except ApiNotAuthenticated:
                return json.dumps({'Error': 'Invalid authentication token'})
            except NoApiTokenFound:
                return json.dumps({'Error': 'Authentication token not found'})

        return self.serialize()
    
    def load_request(self, request):
        self.request = request
        return self
