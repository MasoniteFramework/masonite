import json

from ..helpers import Dot
from ..request import Request
from ..response import Response


class MockRoute:
    def __init__(self, route, container, wsgi=None):
        self.route = route
        self.container = container
        self.wsgi = wsgi

    def assertIsNamed(self, name):
        assert self.route.named_route == name, "Route name is {}. Asserted {}".format(
            self.route.named_route, name
        )
        return self

    def assertIsNotNamed(self):
        assert self.route.named_route is None, "Route has a name: {}".format(
            self.route.named_route
        )
        return self

    def isNamed(self, name):
        return self.route.named_route == name

    def hasMiddleware(self, *middleware):
        return all(elem in self.route.list_middleware for elem in middleware)

    def hasController(self, controller):
        return self.route.controller == controller

    def assertHasController(self, controller):
        if isinstance(controller, str) and "@" in controller:
            controller, method = controller.split("@")
            assert (
                self.route.controller.__name__ == controller
            ), "Controller is {}. Asserted {}".format(
                self.route.controller.__name__, controller
            )
            assert (
                self.route.controller_method == method
            ), "Controller method is {}. Asserted {}".format(
                self.route.controller_method, method
            )

        return self

    def contains(self, value):
        return value in self.container.make(Response).content.decode("utf-8")

    def assertContains(self, value):
        assert self.contains(value), "Response does not contain {}".format(value)
        return self

    def assertNotFound(self):
        return self.assertIsStatus(404)

    def ok(self):
        return "200 OK" in self.container.make(Response).get_status_code()

    def canView(self):
        return self.ok()

    def get_string_response(self):
        response = self.container.make(Response).content

        if isinstance(response, str):
            return response

        return response.decode("utf-8")

    def hasJson(self, key, value=""):

        response = json.loads(self.get_string_response())
        if isinstance(key, dict):
            for item_key, key_value in key.items():
                if not Dot().dot(item_key, response, False) == key_value:
                    return False
            return True
        return Dot().dot(key, response, False)

    def assertHasJson(self, key, value):
        response = json.loads(self.get_string_response())
        if isinstance(key, dict):
            for item_key, key_value in key.items():
                assert Dot().dot(item_key, response, False) == key_value
        else:
            assert (
                Dot().dot(key, response, False) == value
            ), "Key '{}' with the value of '{}' could not find a match in {}".format(
                key, value, response
            )
        return self

    def assertJsonContains(self, key, value):
        response = json.loads(self.get_string_response())
        if not isinstance(response, list):
            raise ValueError(
                "This method can only be used if the response is a list of elements."
            )

        found = False
        for element in response:
            if Dot().dot(key, element, False):
                assert Dot().dot(key, element, False)
                found = True

        if not found:
            raise AssertionError(
                "Could not find a key of: {} that had the value of {}".format(
                    key, value
                )
            )
        return self

    def count(self, amount):
        return len(json.loads(self.get_string_response())) == amount

    def assertCount(self, amount):
        response_amount = len(json.loads(self.get_string_response()))
        assert (
            response_amount == amount
        ), "Response has an count of {}. Asserted {}".format(response_amount, amount)
        return self

    def amount(self, amount):
        return self.count(amount)

    def hasAmount(self, key, amount):
        response = json.loads(self.get_string_response())
        try:
            return len(response[key]) == amount
        except TypeError:
            raise TypeError(
                "The json response key of: {} is not iterable but has the value of {}".format(
                    key, response[key]
                )
            )

    def assertHasAmount(self, key, amount):
        response = json.loads(self.get_string_response())
        try:
            assert len(response[key]) == amount, "{} is not equal to {}".format(
                len(response[key]), amount
            )
        except TypeError:
            raise TypeError(
                "The json response key of: {} is not iterable but has the value of {}".format(
                    key, response[key]
                )
            )

        return self

    def assertNotHasAmount(self, key, amount):
        response = json.loads(self.get_string_response())
        try:
            assert (
                not len(response[key]) == amount
            ), "{} is equal to {} but should not be".format(len(response[key]), amount)
        except TypeError:
            raise TypeError(
                "The json response key of: {} is not iterable but has the value of {}".format(
                    key, response[key]
                )
            )

        return self

    def user(self, obj):
        self._user = obj
        self.container.on_resolve(Request, self._bind_user_to_request)
        return self

    def isPost(self):
        return "POST" in self.route.method_type

    def isGet(self):
        return "GET" in self.route.method_type

    def isPut(self):
        return "PUT" in self.route.method_type

    def isPatch(self):
        return "PATCH" in self.route.method_type

    def isDelete(self):
        return "DELETE" in self.route.method_type

    def on_bind(self, obj, method):
        self.container.on_bind(obj, method)
        return self

    def hasSession(self, key):
        return self.container.make("Session").has(key)

    def assertParameterIs(self, key, value):
        request = self.container.make("Request")
        if key not in request.url_params:
            raise AssertionError(
                "Request class does not have the '{}' url parameter".format(key)
            )

        if request.param(key) != value:
            raise AssertionError(
                "parameter {} is equal to {} of type {}, not {} of type {}".format(
                    key,
                    request.param(key),
                    type(request.param(key)),
                    value,
                    type(value),
                )
            )

    def assertIsStatus(self, status):
        response = self.container.make(Response)
        assert response.is_status(status), AssertionError(
            "{} is not equal to {}".format(response.get_status_code(), status)
        )
        if not response.is_status(status):
            raise AssertionError(
                "{} is not equal to {}".format(response.get_status_code(), status)
            )

        return self

    def assertHasHeader(self, key):
        response = self.container.make(Response)
        assert response.header(key), "Header '{}' does not exist".format(key)
        return self

    def assertNotHasHeader(self, key):
        request = self.container.make("Request")
        assert not request.header(
            key
        ), "Header '{}' exists but asserting it should not".format(key)
        return self

    def assertHeaderIs(self, key, value):
        response = self.container.make(Response)

        header = response.header(key)
        if not header:
            raise ValueError(f"Header {key} is not set")
        if header:
            header = header.value

        assert header == str(value), AssertionError(
            "{} is not equal to {}".format(header, value)
        )

        return self

    def assertPathIs(self, url):
        path = self.container.make("Request").path
        assert path == url, "Asserting the path is '{}' but it is '{}'".format(
            url, path
        )
        return True

    def session(self, key):
        return self.container.make("Session").get(key)

    def on_make(self, obj, method):
        self.container.on_make(obj, method)
        return self

    def on_resolve(self, obj, method):
        self.container.on_resolve(obj, method)
        return self

    def _bind_user_to_request(self, request, container):
        request.set_user(self._user)
        return self

    def headerIs(self, key, value):
        response = self.container.make(Response)
        header = response.header(key)
        if not header:
            raise AssertionError(f"Could not found the {header} header")
        assertion = header.value == value
        if not assertion:
            raise AssertionError(
                "header {} does not equal {}".format(response.header(key), value)
            )
        return assertion

    def parameterIs(self, key, value):
        request = self.container.make("Request")
        assertion = request.param(key) == value
        if not assertion:
            raise AssertionError(
                "parameter {} is equal to {} of type {}, not {} of type {}".format(
                    key,
                    request.param(key),
                    type(request.param(key)),
                    value,
                    type(value),
                )
            )
        return assertion

    @property
    def request(self):
        return self.container.make("Request")

    @property
    def response(self):
        """Gets the string response from the container. This isinstance check here
        is to support Python 3.5. Once python3.5 goes away we can can remove this check.

        @required for 3.5

        Returns:
            string
        """
        response = self.get_string_response()
        if isinstance(response, str):
            return response

        return response.decode("utf-8")

    def asDictionary(self):
        try:
            return json.loads(self.response)
        except ValueError:
            raise ValueError("The response was not json serializable")
