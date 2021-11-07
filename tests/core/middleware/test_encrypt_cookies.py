from tests import TestCase
from src.masonite.middleware import EncryptCookies


class TestEncryptCookiesMiddleware(TestCase):
    def test_encrypts_cookies(self):
        request = self.make_request(
            {"HTTP_COOKIE": f"test={self.application.make('sign').sign('value')}"}
        )

        response = self.make_response()
        EncryptCookies().before(request, None)
        self.assertEqual(request.cookie("test"), "value")

        response.cookie("test", "value")
        EncryptCookies().after(request, response)
        self.assertNotEqual(response.cookie("test"), "value")
