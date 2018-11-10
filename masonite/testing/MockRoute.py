import io

from masonite.app import App
from masonite.request import Request
from masonite.testsuite import TestSuite, generate_wsgi


class MockRoute:

    def __init__(self, route, container):
        self.route = route
        self.container = container

    def is_named(self, name):
        return self.route.named_route == name

    def has_middleware(self, *middleware):
        return all(elem in self.route.list_middleware for elem in middleware)

    def has_controller(self, controller):
        return self.route.controller == controller

    def contains(self, value):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['REQUEST_METHOD'] = self.route.method_type[0]
        self.container = self._run_container(wsgi).container

        return value in self.container.make('Response')

    def status(self, value=None):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['REQUEST_METHOD'] = self.route.method_type[0]
        self.container = self._run_container(wsgi).container

        if not value:
            return self.container.make('Request').get_status_code()

        return self.container.make('Request').get_status_code() == value

    def ok(self):
        return self.status('200 OK')

    def can_view(self):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['RAW_URI'] = self.route.route_url
        self.container = self._run_container(wsgi).container

        return self.container.make('Request').get_status_code() == '200 OK'

    def user(self, obj):
        self._user = obj
        self.container.on_resolve(Request, self._bind_user_to_request)
        return self

    def is_post(self):
        return 'POST' in self.route.method_type

    def is_get(self):
        return 'GET' in self.route.method_type

    def is_put(self):
        return 'PUT' in self.route.method_type

    def is_patch(self):
        return 'PATCH' in self.route.method_type

    def is_delete(self):
        return 'DELETE' in self.route.method_type

    def on_bind(self, obj, method):
        self.container.on_bind(obj, method)
        return self

    def has_session(self, key):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['RAW_URI'] = self.route.route_url
        self.container = self._run_container(wsgi).container
        return self.container.make('Session').has(key)

    def session(self, key):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['RAW_URI'] = self.route.route_url
        self.container = self._run_container(wsgi).container
        return self.container.make('Session').get(key)

    def on_make(self, obj, method):
        self.container.on_make(obj, method)
        return self

    def on_resolve(self, obj, method):
        self.container.on_resolve(obj, method)
        return self

    def _run_container(self, wsgi):
        return TestSuite().create_container(wsgi, container=self.container)

    def _bind_user_to_request(self, request, container):
        request.set_user(self._user)
        return self
