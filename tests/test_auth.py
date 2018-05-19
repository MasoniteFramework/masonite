from masonite.facades.Auth import Auth
from masonite.request import Request

class TestAuth:

    def setup_method(self):
        REQUEST = Request({})

        self.AUTH = Auth(REQUEST, object)

    def test_auth(self):
        assert self.AUTH
