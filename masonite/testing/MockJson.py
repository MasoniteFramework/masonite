from masonite.testsuite import TestSuite, generate_wsgi


class MockJson:

    def __init__(self, url, container):
        self.url = url
        self.container = container

    def status(self, value):
        return self.container.make('Request').get_status_code() == value

    def json(self, request_method, url, data):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = url
        wsgi['CONTENT_TYPE'] = 'application/json'

    def user(self, obj):
        self._user = obj
        self.container.on_resolve('Request', self._bind_user_to_request)
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.url
        self._run_container(wsgi)

        return self

    def contains(self, value):
        return value in self.container.make('Response')

    def _run_container(self, wsgi):
        return TestSuite().create_container(wsgi, container=self.container)

    def _bind_user_to_request(self, request, container):
        request.set_user(self._user)
        return self
