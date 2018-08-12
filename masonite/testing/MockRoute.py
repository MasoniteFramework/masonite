from masonite.testsuite import generate_wsgi, TestSuite
from masonite.app import App

class MockRoute:
    _bind = {}

    def __init__(self, route, container):
        self.route = route
        self.container = container

    def is_named(self, name):
        return self.route.named_route == name

    def has_middleware(self, *middleware):
        return all(elem in self.route.list_middleware for elem in middleware)

    def has_controller(self, controller):
        return self.route.controller == controller

    def can_view(self):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['RAW_URI'] = self.route.route_url
        self.container = self._run_container(wsgi).container

        return self.container.make('Request').get_status_code() == '200 OK'

    def user(self, obj):
        self._user = obj
        self.container.on_bind('Request', self._bind_user_to_request)
        return self
        
    def _run_container(self, wsgi):
        print('======== running =========')
        return TestSuite().create_container(wsgi, container=self.container)
    
    def _bind_user_to_request(self, request, container):
        print('loading user', self._user)
        request.set_user(self._user)   
        return self  
