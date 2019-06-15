from masonite.testsuite import TestSuite
from masonite.testing import BaseRequest


class MockRequest(BaseRequest):

    def __init__(self, url, container):
        self.url = url
        self.container = container

    def _run_container(self, wsgi):
        return TestSuite().create_container(wsgi, container=self.container)

    def _bind_user_to_request(self, request, container):
        request.set_user(self._user)
        return self

    def contains(self, value):
        print('response:', self.container.make('Response'))
        return value in self.container.make('Response')
