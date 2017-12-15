from app.http.providers.request import Request
import json
import re
from playhouse.shortcuts import model_to_dict

class Route():

    def __init__(self, environ):
        self.url = environ['PATH_INFO']

    def get(self, route, output = None):
        # if (self.url == route):
        return output
        # return None

class Get():

    def __init__(self):
        self.method_type = 'GET'
        self.continueroute = True

    def route(self, route, output):
        self.output = output
        self.route = route
        return self

    def middleware(self, middleware):
        if middleware:
            self.continueroute = True
        else:
            self.continueroute = False
        return self

class Post():
    def __init__(self):
        self.method_type = 'POST'
        self.continueroute = True

    def route(self, route, output):
        self.output = output
        self.route = route
        return self

    def middleware(self, middleware):
        if middleware:
            self.continueroute = True
        else:
            self.continueroute = False
        return self

class Api():
    ''' API class docstring '''
    def __init__(self):  
        self.method_type = 'POST'
        self.continueroute = True
        self.url = False
        self.exclude_list = False

    def route(self, route):
        self.url = route
        return self

    def model(self, model):
        # set the default route url
        if not self.url:
            self.url = '/api/' +model.__name__.lower()
            print 'the route is ' + self.url

        self.model_obj = model
        return self

    def fetch(self, request):
        # regex for /api/users/1
        matchregex = re.compile("^\/\w+\/\w+\/(\d+)")
        updateregex = re.compile("^\/\w+\/\w+\/(\d+)/update")
        match_url = matchregex.match(request.path)
        match_update_url = updateregex.match(request.path)

        if self.url == request.path and request.method == 'GET':
            # if GET /api/user
            if self.exclude_list:
                for attribute in self.exclude_list:
                    delattr(self.model_obj, attribute)
            query = self.model_obj.select().order_by(self.model_obj.name).dicts()
            self.output =  json.dumps({'rows': list(query)})
        elif match_url and request.method == 'GET':
            # if GET /api/user/1
            query = self.model_obj.get(self.model_obj.id == match_url.group(1))
            self.output = json.dumps(model_to_dict(query))
        elif self.url == request.path and request.method == 'POST':
            # if POST /api/user
            proxy = self.model_obj()
            for field in request.all():
                setattr(proxy, field, request.input(field))
            proxy.save()
            self.output = json.dumps(model_to_dict(proxy))
        elif match_url and request.method == 'DELETE':
            # if DELETE /api/user
            get = self.model_obj.get(self.model_obj.id == match_url.group(1))
            query = self.model_obj.delete().where(self.model_obj.id == match_url.group(1))
            query.execute()
            self.output = json.dumps(model_to_dict(get))
        elif match_update_url and request.method == 'POST':
            # if POST /api/user/1/update
            proxy = self.model_obj.get(self.model_obj.id == match_update_url.group(1))
            for field in request.all():
                setattr(proxy, field, request.input(field))
            proxy.save()
            proxy = self.model_obj.get(self.model_obj.id == match_update_url.group(1))
            self.output = json.dumps(model_to_dict(proxy))
        else:
            self.output = None
        return self

    def exclude(self, exclude_list):
        self.exclude_list = exclude_list
        return self
