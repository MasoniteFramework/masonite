from tests import TestCase
from src.masonite.api.authentication import AuthenticatesTokens


class MockModel(AuthenticatesTokens):
    def save(self, *args, **kwargs):
        pass


class TestApiModule(TestCase):
    def test_can_generate_token(self):
        user = MockModel()

        self.assertTrue(len(user.generate_jwt()) == 166)
