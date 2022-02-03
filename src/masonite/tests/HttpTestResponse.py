import json
from ..views import View
from ..controllers import Controller
from ..utils.structures import data_get


class HttpTestResponse:
    def __init__(self, application, request, response, route):
        self.application = application
        self.request = request
        self.response = response
        self.route = route
        self.content = None
        self.status = None
        self.get_response()

    def get_response(self):
        self.content = self.response.get_response_content()
        return self

    def get_content(self):
        """Take care of decoding content if bytes and returns str."""
        return (
            self.content.decode("utf-8")
            if isinstance(self.content, bytes)
            else str(self.content)
        )

    def assertContains(self, content):
        assert (
            content in self.get_content()
        ), f"{content} not found in {self.get_content()}"
        return self

    def assertNotContains(self, content):
        assert content not in self.get_content()
        return self

    def assertContainsInOrder(self, *content):
        response_content = self.get_content()
        index = 0
        for content_string in content:
            found_at_index = response_content.find(content_string, index)
            assert found_at_index != -1
            index = found_at_index + len(content_string)
        return self

    def assertIsNamed(self, name):
        assert (
            self.route.get_name() == name
        ), f"Route name is {self.route.get_name()}. Asserted {name}"
        return self

    def assertIsNotNamed(self, name=None):
        if name is None:
            assert self.route.name is None, "Route has a name: {}".format(
                self.route.name
            )
        else:
            assert (
                self.route.get_name() != name
            ), f"Route name {self.route.get_name()} matches expected {name}"
        return self

    def assertIsStatus(self, status):
        assert self.response.is_status(
            status
        ), f"Status is {self.response.get_status_code()}. Asserted {status}"
        return self

    def assertNotFound(self):
        return self.assertIsStatus(404)

    def assertOk(self):
        return self.assertIsStatus(200)

    def assertCreated(self):
        return self.assertIsStatus(201)

    def assertSuccessful(self):
        assert 200 <= self.response.get_status_code() < 300
        return self

    def assertNoContent(self, status=204):
        assert not self.get_content()
        return self.assertIsStatus(status)

    def assertUnauthorized(self):
        return self.assertIsStatus(401)

    def assertForbidden(self):
        return self.assertIsStatus(403)

    def assertError(self):
        return self.assertIsStatus(500)

    def assertHasHeader(self, name, value=None):
        header_value = self.response.header(name)
        assert header_value, f"Could not find the header {name}"
        if value:
            assert value == header_value, f"Header '{name}' does not equal {value}"

    def assertHeaderMissing(self, name):
        assert not self.response.header(name)

    def assertLocation(self, location):
        return self.assertHasHeader("Location", location)

    def assertRedirect(self, url=None, name=None, params={}):
        # we could assert 301 or 302 code => what if user uses another status code in redirect()
        # here we are sure
        assert self.get_content() == "Redirecting ..."
        if url:
            self.assertLocation(url)
        elif name:
            url = self.response._get_url_from_route_name(name, params)
            self.assertLocation(url)
        return self

    def assertCookie(self, name, value=None):
        assert self.request.cookie_jar.exists(name)
        if value is not None:
            assert self.request.cookie_jar.get(name).value == value
        return self

    def assertPlainCookie(self, name):
        assert self.request.cookie_jar.exists(name)
        assert not self.request.cookie_jar.get(name).secure
        return self

    def assertCookieExpired(self, name):
        self.assertCookie(name)
        assert self.request.cookie_jar.is_expired(name)
        return self

    def assertCookieNotExpired(self, name):
        return not self.assertCookieExpired(name)

    def assertCookieMissing(self, name):
        assert not self.request.cookie_jar.exists(name)
        return self

    def assertSessionHas(self, key, value=None):
        """Assert that session contains the given key with the corresponding value if given.
        The session driver can be specified if necessary."""
        session = self.request.session
        assert session.has(key)
        if value is not None:
            assert session.get(key) == value
        return self

    def assertSessionMissing(self, key):
        """Assert that session does not contain the given key. The session driver can be specified
        if necessary."""
        assert not self.request.session.get(key)
        return self

    def assertSessionHasErrors(self, keys=[]):
        """Assert that session contains errors for the given list of keys (meaning that each given key
        exists in 'errors' dict in session.) If no keys are given this will assert that the
        sessions has errors without checking specific keys."""
        session = self.request.session
        assert session.has("errors")
        if keys:
            errors = session.get("errors")
            for key in keys:
                assert errors.get(key)
        return self

    def assertSessionHasNoErrors(self, keys=[]):
        """Assert that session does not have any errors (meaning that session does not contain an
        'errors' key or 'errors' key is empty. If a list of keys is given, this will check
        that there are no errors for each of those keys."""
        session = self.request.session
        if not keys:
            assert not session.has("errors")
        else:
            errors = session.get("errors")
            for key in keys:
                assert not errors.get(key)
        return self

    def _ensure_response_has_view(self):
        """Ensure that the response has a view as its original content."""
        if not (self.response.original and isinstance(self.response.original, View)):
            raise ValueError("The response is not a view")

    def assertViewIs(self, name):
        """Assert that request renders the given view name."""
        self._ensure_response_has_view()
        assert (
            self.response.original.template == name
        ), f"Template {self.response.original.template} is not equal to {name}"
        return self

    def assertViewHas(self, key, value=None):
        """Assert that view context contains a given data key (and eventually associated value)."""
        self._ensure_response_has_view()
        value_at_key = data_get(self.response.original.dictionary, key)
        assert value_at_key
        if value:
            assert value_at_key == value
        return self

    def assertViewHasExact(self, keys):
        """Assert that view context contains exactly the data keys (or the complete data dict)."""
        self._ensure_response_has_view()
        if isinstance(keys, list):
            assert set(keys) == set(self.response.original.dictionary.keys()) - set(
                self.response.original._shared.keys()
            )
        else:
            view_data = self.response.original.dictionary
            for key in self.response.original._shared:
                del view_data[key]
            assert keys == view_data
        return self

    def assertViewMissing(self, key):
        """Assert that given data key is not in the view context."""
        self._ensure_response_has_view()
        assert not data_get(self.response.original.dictionary, key)
        return self

    def assertAuthenticated(self):
        assert self.application.make("auth").guard("web").user()
        return self

    def assertGuest(self):
        assert not self.application.make("auth").guard("web").user()
        return self

    def assertAuthenticatedAs(self, user):
        user = self.application.make("auth").guard("web").user()
        assert user == user
        return self

    def assertHasHttpMiddleware(self, middleware):
        """Assert that the request/response cycle has the given middleware. The HTTP middleware
        class should be given."""
        assert middleware in self.application.make("middleware").http_middleware
        return self

    def assertHasRouteMiddleware(self, middleware):
        """Assert that the route has the given middleware. The registration key of the middleware
        should be used."""
        assert middleware in self.application.make("middleware").route_middleware
        return self

    def assertHasController(self, controller):
        """Assert that route used the given controller. The controller can be a class or
        a string. If it's a string it should be formatted as follow: ControllerName@method"""
        if isinstance(controller, str) and "@" in controller:
            assert self.route.controller == controller
        elif issubclass(controller, Controller):
            assert self.route.controller_class == controller
        else:
            raise ValueError(
                "controller must be a string like YourController@index or a Controller class"
            )
        return self

    def assertRouteHasParameter(self, key, value=None):
        assert key in self.route.url_list, "Route does not contain parameter {key}."
        if value is not None:
            assert self.request.param(key) == str(value)
            pass
        return self

    def _ensure_response_is_json(self):
        """Parse response back from JSON into a dict, if an error happens the response was not
        a JSON string."""
        try:
            return json.loads(self.response.content)
        except ValueError:
            raise ValueError("The response was not JSON serializable")

    def assertJson(self, data={}):
        """Assert that response is JSON and contains the given data dictionary. The assertion will
        pass even if it is not an exact match."""
        response_data = self._ensure_response_is_json()
        assert data.items() <= response_data.items()
        return self

    def assertJsonPath(self, path, value=None):
        """Assert that response is JSON and contains the given path, with eventually the given
        value if provided. The path is a dotted path."""
        response_data = self._ensure_response_is_json()
        data_at_path = data_get(response_data, path)

        assert data_at_path == value, f"'{data_at_path}' does not equal {value}"
        return self

    def assertJsonExact(self, data):
        """Assert that response is JSON and is exactly the given data."""
        response_data = self._ensure_response_is_json()
        assert response_data == data, f"'{response_data}' does not equal {data}"
        return self

    def assertJsonCount(self, count, key=None):
        """Assert that JSON response is JSON and has the given count of keys at root level
        or at the given key."""
        response_data = self._ensure_response_is_json()
        if key is not None:
            response_data = response_data.get(key, {})

        response_count = len(response_data.keys())
        assert (
            response_count == count
        ), f"JSON response count is {response_count}. Asserted {count}."
        return self

    def assertJsonMissing(self, path):
        """Assert that JSON response is JSON and does not contain given path.
        The path can be a dotted path"""
        response_data = self._ensure_response_is_json()
        assert not data_get(
            response_data, path
        ), f"'{response_data}' is not missing from {data_get(response_data, path)}"
        return self
