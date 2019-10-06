from masonite.request import Request
from masonite.testsuite import TestSuite, generate_wsgi
import json
from masonite.helpers import Dot


class MockRoute:

    def __init__(self, route, container, wsgi=None):
        self.route = route
        self.container = container
        self.wsgi = wsgi

    def isNamed(self, name):
        return self.route.named_route == name

    def hasMiddleware(self, *middleware):
        return all(elem in self.route.list_middleware for elem in middleware)

    def hasController(self, controller):
        return self.route.controller == controller

    def contains(self, value):
        return value in self.container.make('Response')

    def assertContains(self, value):
        assert value in self.container.make('Response'), "Response does not contain {}".format(value)
        return self

    def assertNotFound(self):
        return self.assertIsStatus(404)

    def ok(self):
        return '200 OK' in self.container.make('Request').get_status_code()

    def canView(self):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['RAW_URI'] = self.route.route_url
        self.container = self._run_container(wsgi).container

        return self.container.make('Request').get_status_code() == '200 OK'

    def hasJson(self, key, value=''):
        response = json.loads(self.container.make('Response'))
        if isinstance(key, dict):
            for item_key, key_value in key.items():
                if not Dot().dot(item_key, response, False) == key_value:
                    return False
            return True
        return Dot().dot(key, response, False)

    def assertHasJson(self, key, value):
        response = json.loads(self.container.make('Response'))
        if isinstance(key, dict):
            for item_key, key_value in key.items():
                assert Dot().dot(item_key, response, False) == key_value
        else:
            assert Dot().dot(key, response, False) == value, "Key '{}' with the value of '{}' could not find a match in {}".format(key, value, response)
        return self

    def assertJsonContains(self, key, value):
        response = json.loads(self.container.make('Response'))
        if not isinstance(response, list):
            raise ValueError("This method can only be used if the response is a list of elements.")

        found = False
        for element in response:
            if Dot().dot(key, element, False):
                assert Dot().dot(key, element, False)
                found = True

        if not found:
            raise AssertionError("Could not find a key of: {} that had the value of {}".format(key, value))
        return self

    def count(self, amount):
        return len(json.loads(self.container.make('Response'))) == amount

    def assertCount(self, amount):
        response_amount = len(json.loads(self.container.make('Response')))
        assert response_amount == amount, 'Response has an count of {}. Asserted {}'.format(response_amount, amount)
        return self

    def amount(self, amount):
        return self.count(amount)

    def hasAmount(self, key, amount):
        response = json.loads(self.container.make('Response'))
        try:
            return len(response[key]) == amount
        except TypeError:
            raise TypeError("The json response key of: {} is not iterable but has the value of {}".format(key, response[key]))

    def assertHasAmount(self, key, amount):
        response = json.loads(self.container.make('Response'))
        try:
            assert len(response[key]) == amount, '{} is not equal to {}'.format(len(response[key]), amount)
        except TypeError:
            raise TypeError("The json response key of: {} is not iterable but has the value of {}".format(key, response[key]))

        return self

    def assertNotHasAmount(self, key, amount):
        response = json.loads(self.container.make('Response'))
        try:
            assert not len(response[key]) == amount, '{} is equal to {} but should not be'.format(len(response[key]), amount)
        except TypeError:
            raise TypeError("The json response key of: {} is not iterable but has the value of {}".format(key, response[key]))

        return self

    def user(self, obj):
        self._user = obj
        self.container.on_resolve(Request, self._bind_user_to_request)
        return self

    def isPost(self):
        return 'POST' in self.route.method_type

    def isGet(self):
        return 'GET' in self.route.method_type

    def isPut(self):
        return 'PUT' in self.route.method_type

    def isPatch(self):
        return 'PATCH' in self.route.method_type

    def isDelete(self):
        return 'DELETE' in self.route.method_type

    def on_bind(self, obj, method):
        self.container.on_bind(obj, method)
        return self

    def hasSession(self, key):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.route.route_url
        wsgi['RAW_URI'] = self.route.route_url
        self.container = self._run_container(wsgi).container
        return self.container.make('Session').has(key)

    def assertParameterIs(self, key, value):
        request = self.container.make('Request')
        if key not in request.url_params:
            raise AssertionError("Request class does not have the '{}' url parameter".format(key))

        if request.param(key) != value:
            raise AssertionError('parameter {} is equal to {} of type {}, not {} of type {}'.format(key, request.param(key), type(request.param(key)), value, type(value)))

    def assertIsStatus(self, status):
        request = self.container.make('Request')
        assert request.is_status(status), AssertionError("{} is not equal to {}".format(request.get_status_code(), status))
        if not request.is_status(status):
            raise AssertionError("{} is not equal to {}".format(request.get_status_code(), status))

        return self

    def assertHasHeader(self, key):
        pass

    def assertHeaderIs(self, key, value):
        request = self.container.make('Request')
        assert str(request.header(key)) == str(value), AssertionError("{} is not equal to {}".format(request.header(key), value))

        return self

    def assertPathIs(self, url):
        path = self.container.make('Request').path
        assert path == url, "Asserting the path is '{}' but it is '{}'".format(url, path)
        return True

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

    def headerIs(self, key, value):
        request = self.container.make('Request')
        assertion = request.header(key) == value
        if not assertion:
            raise AssertionError('header {} does not equal {}'.format(request.header(key), value))
        return assertion

    def parameterIs(self, key, value):
        request = self.container.make('Request')
        assertion = request.param(key) == value
        if not assertion:
            raise AssertionError('parameter {} is equal to {} of type {}, not {} of type {}'.format(key, request.param(key), type(request.param(key)), value, type(value)))
        return assertion

    @property
    def request(self):
        return self.container.make('Request')

    @property
    def response(self):
        return self.container.make('Response')

    def asDictionary(self):
        try:
            return json.loads(self.response)
        except ValueError:
            raise ValueError("The response was not json serializable")
