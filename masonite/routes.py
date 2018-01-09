''' Module for the Routing System '''
import json
import re
import importlib

class Route():
    ''' Loads the environ '''

    def __init__(self, environ):
        self.url = environ['PATH_INFO']

    def get(self, route, output=None):
        ''' Returns the output '''
        return output

class Get():
    ''' Class for specifying GET requests '''

    def __init__(self):
        self.method_type = 'GET'
        self.continueroute = True
        self.output = False
        self.route_url = None
        self.named_route = None

    def route(self, route, output):
        ''' The model route given by the developer.
            The output parameter is a controller and method
        '''

        if isinstance(output, str):
            mod = output.split('@')

            # import the module
            module = importlib.import_module('app.http.controllers.' + mod[0])

            # get the controller from the module
            controller = getattr(module, mod[0])

            # get the view from the controller
            view = getattr(controller(), mod[1])
            self.output = view
        else:
            self.output = output

        self.route_url = route
        return self

    def middleware(self, middleware):
        ''' Blocking middleware '''
        self.continueroute = bool(middleware)
        return self

    def name(self, name):
        self.named_route = name
        return self

class Post():
    ''' Class for specifying POST requests '''

    def __init__(self):
        self.method_type = 'POST'
        self.continueroute = True
        self.output = False
        self.route_url = None

    def route(self, route, output):
        ''' Loads the route into the class '''

        if isinstance(output, str):
            mod = output.split('@')

            # import the module
            module = importlib.import_module('app.http.controllers.' + mod[0])

            # get the controller from the module
            controller = getattr(module, mod[0])

            # get the view from the controller
            view = getattr(controller(), mod[1])
            self.output = view
        else:
            self.output = output
        self.route_url = route
        return self

    def middleware(self, middleware):
        ''' Blocking middleware '''
        self.continueroute = bool(middleware)
        return self

class Api():
    ''' API class docstring '''
    def __init__(self):
        self.method_type = 'POST'
        self.continueroute = True
        self.url = False
        self.exclude_list = False
        self.output = False
        self.model_obj = None

    def route(self, route):
        ''' Loads the route into the class '''
        self.url = route
        return self

    def model(self, model):
        ''' Loads the model into the class '''
        if not self.url:
            self.url = '/api/' +model.__name__.lower()
            print('the route is ' + self.url)

        self.model_obj = model
        return self

    def fetch(self, request):
        ''' Fetch the API from the model '''
        # regex for /api/users/1
        matchregex = re.compile(r"^\/\w+\/\w+\/(\d+)")
        updateregex = re.compile(r"^\/\w+\/\w+\/(\d+)/update")
        match_url = matchregex.match(request.path)
        match_update_url = updateregex.match(request.path)

        if self.url == request.path and request.method == 'GET':
            # if GET /api/user

            model = self.model_obj
            model.__hidden__ = self.exclude_list

            query = model.all()

            self.output = query.to_json()
        elif match_url and request.method == 'GET':
            # if GET /api/user/1
            # query = self.model_obj.get(self.model_obj.id == match_url.group(1))
            model = self.model_obj.find(match_url.group(1))
            if model:
                self.output = model.to_json()
            else:
                self.output = []
        elif self.url == request.path and request.method == 'POST':
            # if POST /api/user
            proxy = self.model_obj()
            for field in request.all():
                setattr(proxy, field, request.input(field))
            proxy.save()
            self.output = proxy.to_json()
        elif match_url and request.method == 'DELETE':
            # if DELETE /api/user/1
            get = self.model_obj.find(match_url.group(1))
            if get:
                query = get.delete()
                self.output = get.to_json()
            else:
                self.output = []
        elif match_update_url and request.method == 'POST':
            # if POST /api/user/1/update
            proxy = self.model_obj.find(match_update_url.group(1))
            for field in request.all():
                setattr(proxy, field, request.input(field))
            proxy.save()
            proxy = self.model_obj.find(match_update_url.group(1))
            self.output = proxy.to_json()
        else:
            self.output = None
        return self

    def exclude(self, exclude_list):
        ''' Exclude columns from the model '''
        self.exclude_list = exclude_list
        return self
