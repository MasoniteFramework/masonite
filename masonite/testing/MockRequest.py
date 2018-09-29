from masonite.testsuite import TestSuite, generate_wsgi
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
