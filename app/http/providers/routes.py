from app.http.providers.request import Request

class Route():

    def __init__(self, environ):
        self.url = environ['PATH_INFO']

    def get(self, route, output):
        if (self.url == route):
            return output
        return None

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
