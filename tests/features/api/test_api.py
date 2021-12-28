from tests import TestCase
from src.masonite.api.facades import Api
from src.masonite.headers import Header


class TestApiModule(TestCase):
    def test_can_get_token_from_input(self):
        request = self.make_request()
        request.input_bag.add_post("token", "secret")

        self.assertEqual(Api.get_token(), "secret")

    def test_can_get_token_from_header(self):
        request = self.make_request()
        request.header_bag.add(Header("Authorization", "Bearer secret-header-key"))

        self.assertEqual(Api.get_token(), "secret-header-key")
